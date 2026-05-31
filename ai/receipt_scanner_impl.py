import logging
import os
import re
import json
import shutil
from pathlib import Path
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

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

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[ReceiptScanner] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if load_dotenv is not None:
    env_path = Path(__file__).resolve().parents[1] / '.env'
    if env_path.exists():
        logger.debug(f"Loading .env from {env_path}")
        load_dotenv(dotenv_path=env_path, override=False)
    else:
        logger.debug("No .env file found at project root; skipping dotenv load.")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[ReceiptScanner] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

TESSERACT_ENV_VARS = [
    "TESSERACT_CMD",
    "TESSERACT_PATH",
    "TESSERACT",
    "TESSERACT_EXE",
]

COMMON_TESSERACT_PATHS = [
    # Windows common installers
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
    r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
    # macOS Brew / default
    "/opt/homebrew/bin/tesseract",
    "/usr/local/bin/tesseract",
    "/usr/bin/tesseract",
    # Linux defaults
    "/usr/bin/tesseract",
    "/usr/local/bin/tesseract",
]


def _is_executable(path: str) -> bool:
    return bool(path and os.path.isfile(path) and os.access(path, os.X_OK))


def _resolve_tesseract_candidate(candidate: str):
    if not candidate:
        return None
    candidate = candidate.strip().strip('"')

    if os.path.isdir(candidate):
        for name in ["tesseract.exe", "tesseract"]:
            candidate_path = os.path.join(candidate, name)
            if _is_executable(candidate_path):
                return candidate_path
        return None

    if _is_executable(candidate):
        return candidate

    return shutil.which(candidate)


def _find_tesseract_cmd(override_cmd=None) -> str:
    candidates = []
    if override_cmd:
        candidates.append(override_cmd)
    for env_var in TESSERACT_ENV_VARS:
        value = os.environ.get(env_var)
        if value:
            logger.debug(f"Found environment variable {env_var}={value}")
            candidates.append(value)

    path_candidate = shutil.which("tesseract")
    if path_candidate:
        logger.debug(f"Found tesseract on PATH: {path_candidate}")
        candidates.append(path_candidate)

    candidates.extend(COMMON_TESSERACT_PATHS)

    for candidate in candidates:
        resolved = _resolve_tesseract_candidate(candidate)
        if resolved:
            logger.debug(f"Resolved Tesseract candidate {candidate} -> {resolved}")
            return resolved
        logger.debug(f"Tesseract candidate not valid: {candidate}")

    logger.debug("No valid Tesseract executable found among candidates.")
    return None


class ReceiptScanner:
    def __init__(self, tesseract_cmd=None):
        self.tesseract_cmd = _find_tesseract_cmd(tesseract_cmd)
        if pytesseract:
            if self.tesseract_cmd:
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
                logger.info(f"Tesseract found and configured at: {self.tesseract_cmd}")
            else:
                logger.warning(
                    "Tesseract executable not found. "
                    "Set TESSERACT_CMD or TESSERACT_PATH, or install Tesseract on your system."
                )
        else:
            logger.warning("pytesseract module is not installed. OCR is unavailable.")

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
        gray = cv2.equalizeHist(gray)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 12
        )
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel, iterations=1)
        return cleaned

    def _order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
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
        dst = np.array(
            [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
            dtype="float32",
        )
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    def _find_receipt_contour(self, img):
        if cv2 is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        height, width = img.shape[:2]
        min_area = width * height * 0.05
        for c in sorted(contours, key=cv2.contourArea, reverse=True):
            area = cv2.contourArea(c)
            if area < min_area:
                continue
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                return approx.reshape(4, 2)
        return None

    def _deskew_and_crop(self, img):
        if cv2 is None:
            return img
        orig = img.copy()
        receipt_contour = self._find_receipt_contour(img)
        if receipt_contour is not None:
            rect = self._order_points(receipt_contour)
            warped = self._four_point_transform(orig, rect)
            return warped
        return orig

    def _ensure_tesseract_available(self):
        if pytesseract is None:
            raise RuntimeError(
                "pytesseract is not installed. Install it with `pip install pytesseract`."
            )
        if not self.tesseract_cmd:
            raise RuntimeError(
                "Tesseract executable not found. Install Tesseract or set TESSERACT_CMD/TESSERACT_PATH. "
                "Common Windows paths: C:\\Program Files\\Tesseract-OCR\\tesseract.exe or C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe."
            )

    def _ocr(self, img):
        self._ensure_tesseract_available()
        try:
            if cv2 is not None:
                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb)
            else:
                pil_img = Image.fromarray(img)
            data = pytesseract.image_to_data(
                pil_img,
                output_type=pytesseract.Output.DICT,
                lang='eng',
                config='--psm 6',
            )
        except Exception as exc:
            if hasattr(pytesseract, 'TesseractNotFoundError') and isinstance(exc, pytesseract.TesseractNotFoundError):
                raise RuntimeError(
                    "Tesseract executable was not found. "
                    "Please install Tesseract or set TESSERACT_CMD/TESSERACT_PATH."
                ) from exc
            logger.exception("OCR processing failed")
            raise RuntimeError(f"OCR processing failed: {exc}") from exc

        lines = []
        confidences = []
        for text, conf in zip(data.get('text', []), data.get('conf', [])):
            if text and text.strip():
                lines.append(text.strip())
                try:
                    conf_value = float(conf)
                except Exception:
                    conf_value = -1.0
                if conf_value >= 0:
                    confidences.append(conf_value)
        average_confidence = float(sum(confidences) / len(confidences)) if confidences else 0.0
        extracted_text = "\n".join(lines)
        return extracted_text, average_confidence, data

    def _has_date(self, lines):
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
            r'\d{2}-\d{2}-\d{4}',
            r'\d{1,2}/\d{1,2}/\d{2,4}',
        ]
        for l in lines:
            for p in date_patterns:
                m = re.search(p, l)
                if m:
                    return m.group(0)
        return None

    def _has_total(self, lines):
        total_patterns = [
            r'(?i)total[^0-9]*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))',
            r'(?i)subtotal[^0-9]*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))',
            r'(\$\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))$',
        ]
        for l in reversed(lines[-15:]):
            for p in total_patterns:
                m = re.search(p, l)
                if m:
                    return m.group(1).replace(',', '').replace('$', '').strip()
        return None

    def _has_tax(self, lines):
        tax_patterns = [
            r'(?i)tax[^0-9]*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))',
            r'(?i)vat[^0-9]*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))',
        ]
        for l in lines:
            for p in tax_patterns:
                m = re.search(p, l)
                if m:
                    return m.group(1).replace(',', '').strip()
        return None

    def _has_store(self, lines):
        if not lines:
            return None
        candidate = lines[0].strip()
        if len(candidate) >= 3 and re.search(r'[A-Za-z]', candidate) and not re.search(r'receipt', candidate, re.I):
            return candidate
        for l in lines[:3]:
            if len(l.strip()) >= 3 and re.search(r'[A-Za-z]', l) and not re.search(r'receipt', l, re.I):
                return l.strip()
        return None

    def _find_item_lines(self, lines):
        item_pattern = re.compile(r'(.+?)\s+(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))$')
        items = []
        for l in lines:
            m = item_pattern.search(l)
            if m:
                name = m.group(1).strip()
                price = m.group(2).replace(',', '').strip()
                try:
                    items.append({'name': name, 'price': float(price)})
                except Exception:
                    continue
        return items

    def _has_currency(self, lines):
        currency_pattern = re.compile(r'(\$|€|£|¥)\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})')
        digits_pattern = re.compile(r'\d+\.?\d{2}')
        for l in lines:
            if currency_pattern.search(l) or digits_pattern.search(l):
                return True
        return False

    def _validate_receipt(self, lines, confidence, receipt_contour_found):
        evidence = {
            'has_store_name': bool(self._has_store(lines)),
            'has_date': bool(self._has_date(lines)),
            'has_total': bool(self._has_total(lines)),
            'has_items': len(self._find_item_lines(lines)) >= 2,
            'has_currency': self._has_currency(lines),
            'has_receipt_shape': bool(receipt_contour_found),
        }
        logger.debug(f"OCR confidence={confidence:.1f}, receipt shape={evidence['has_receipt_shape']}, evidence={evidence}")
        valid = evidence['has_total'] and evidence['has_store_name'] and evidence['has_date'] and evidence['has_items'] and confidence >= 45.0
        if not valid:
            if confidence < 45.0:
                reason = "Low OCR confidence."
            elif not evidence['has_total']:
                reason = "No total/subtotal found."
            elif not evidence['has_items']:
                reason = "Not enough item lines were found."
            elif not evidence['has_date']:
                reason = "No date was detected."
            elif not evidence['has_store_name']:
                reason = "No merchant/store name was detected."
            else:
                reason = "Receipt validation failed."
            return False, evidence, reason
        return True, evidence, "Receipt appears valid."

    def parse_text(self, text, data=None, receipt_contour_found=False):
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        merchant = self._has_store(lines)
        date = self._has_date(lines)
        total = self._has_total(lines)
        tax = self._has_tax(lines)
        payment = None
        payment_keywords = ['visa', 'mastercard', 'amex', 'cash', 'debit', 'credit']
        for l in lines:
            low = l.lower()
            for kw in payment_keywords:
                if kw in low:
                    payment = kw.upper()
                    break
            if payment:
                break
        items = self._find_item_lines(lines)
        confidence = 0.0
        if data is not None and 'conf' in data:
            confidences = []
            for conf in data.get('conf', []):
                try:
                    conf_value = float(conf)
                except Exception:
                    continue
                if conf_value >= 0:
                    confidences.append(conf_value)
            confidence = float(sum(confidences) / len(confidences)) if confidences else 0.0
        valid, evidence, validation_message = self._validate_receipt(lines, confidence, receipt_contour_found)
        return {
            'merchant': merchant,
            'date': date,
            'total': float(total) if total else None,
            'tax': float(tax) if tax else None,
            'payment_method': payment,
            'items': items,
            'ocr_text': text,
            'confidence_score': confidence,
            'evidence': evidence,
            'valid_receipt': valid,
            'validation_message': validation_message,
        }

    def scan(self, path, save_processed=False, processed_path=None):
        img = self._load(path)
        receipt_contour = self._find_receipt_contour(img) if cv2 is not None else None
        warped = self._deskew_and_crop(img)
        processed = self._preprocess(warped) if cv2 is not None else warped
        text, confidence, data = self._ocr(processed)
        parsed = self.parse_text(text, data=data, receipt_contour_found=bool(receipt_contour))
        if save_processed and processed_path:
            try:
                if cv2 is not None:
                    cv2.imwrite(processed_path, processed)
                else:
                    Image.fromarray(processed).save(processed_path)
            except Exception:
                pass
        parsed['image_path'] = path
        return parsed
