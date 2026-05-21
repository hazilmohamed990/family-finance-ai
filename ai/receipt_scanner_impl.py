import os
import re
import json
try:
    import cv2
except Exception:
    cv2 = None
import numpy as np
from PIL import Image
try:
    import pytesseract
except Exception:
    pytesseract = None

class ReceiptScanner:
    def __init__(self, tesseract_cmd=None):
        if pytesseract and tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def _load(self, path):
        if cv2:
            img = cv2.imread(path)
            if img is None:
                raise FileNotFoundError(path)
            return img
        else:
            return np.array(Image.open(path).convert('RGB'))[:, :, ::-1]

    def _preprocess(self, img):
        if cv2 is None:
            return img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 9, 75, 75)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,41,15)
        return thresh

    def _order_points(self, pts):
        rect = np.zeros((4,2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def _four_point_transform(self, image, rect):
        (tl, tr, br, bl) = rect
        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = max(int(widthA), int(widthB))
        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0,maxHeight-1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    def _deskew_and_crop(self, img):
        if cv2 is None:
            return img
        orig = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(5,5),0)
        edged = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                pts = approx.reshape(4,2)
                rect = self._order_points(pts)
                warped = self._four_point_transform(orig, rect)
                return warped
        return orig

    def _ocr(self, img):
        if pytesseract is None:
            return ""
        if cv2 is not None:
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb)
        else:
            pil_img = Image.fromarray(img)
        text = pytesseract.image_to_string(pil_img, lang='eng')
        return text

    def parse_text(self, text):
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        merchant = lines[0] if lines else ""
        date = None
        total = None
        tax = None
        payment = None
        items = []
        date_patterns = [r'\d{4}-\d{2}-\d{2}', r'\d{2}/\d{2}/\d{4}', r'\d{2}-\d{2}-\d{4}']
        for l in lines:
            for p in date_patterns:
                m = re.search(p, l)
                if m:
                    date = m.group(0)
                    break
            if date:
                break
        total_patterns = [r'(?i)total[^0-9]*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))', r'(\d+\.\d{2})$']
        for l in reversed(lines[-12:]):
            for p in total_patterns:
                m = re.search(p, l)
                if m:
                    total = m.group(1).replace(',', '')
                    break
            if total:
                break
        tax_patterns = [r'(?i)tax[^0-9]*(\d+\.\d{2})', r'VAT[^0-9]*(\d+\.\d{2})']
        for l in lines:
            for p in tax_patterns:
                m = re.search(p, l)
                if m:
                    tax = m.group(1).replace(',', '')
                    break
            if tax:
                break
        payment_keywords = ['visa','mastercard','amex','cash','debit']
        for l in lines:
            low = l.lower()
            for kw in payment_keywords:
                if kw in low:
                    payment = kw.upper()
                    break
            if payment:
                break
        item_pattern = re.compile(r'(.+?)\s+(\d+\.\d{2})$')
        for l in lines[1:25]:
            m = item_pattern.search(l)
            if m:
                try:
                    price = float(m.group(2))
                except Exception:
                    price = 0.0
                items.append({'name': m.group(1).strip(), 'price': price})
        result = {'merchant': merchant, 'date': date, 'total': float(total) if total else None, 'tax': float(tax) if tax else None, 'payment_method': payment, 'items': items, 'ocr_text': text}
        return result

    def scan(self, path, save_processed=False, processed_path=None):
        img = self._load(path)
        warped = self._deskew_and_crop(img)
        processed = self._preprocess(warped) if cv2 is not None else warped
        ocr_text = self._ocr(warped)
        parsed = self.parse_text(ocr_text)
        if save_processed and processed_path:
            try:
                if cv2 is not None:
                    cv2.imwrite(processed_path, processed)
                else:
                    Image.fromarray(processed).save(processed_path)
            except Exception:
                pass
        parsed['image_path'] = path
        parsed['ocr_text'] = ocr_text
        return parsed
