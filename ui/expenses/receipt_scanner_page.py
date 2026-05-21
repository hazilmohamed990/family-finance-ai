from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os, shutil
from datetime import datetime, shutil
from datetime import datetime

from ai.receipt_scanner_impl import ReceiptScanner

class ReceiptScannerPage(QWidget):
    def __init__(self, repo, refresh_callbacks=None):
        super().__init__()
        self.repo = repo
        self.refresh_callbacks = refresh_callbacks or []
        self.scanner = ReceiptScanner()
        self.image_path = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        header = QLabel('Receipt Scanner')
        header.setStyleSheet('font-size:24px; font-weight:800;')
        layout.addWidget(header)
        btn_layout = QHBoxLayout()
        self.upload_btn = QPushButton('Upload Image')
        self.upload_btn.clicked.connect(self.upload_image)
        self.scan_btn = QPushButton('Scan Receipt')
        self.scan_btn.clicked.connect(self.scan_receipt)
        self.save_btn = QPushButton('Save to Database')
        self.save_btn.clicked.connect(self.save_receipt)
        btn_layout.addWidget(self.upload_btn)
        btn_layout.addWidget(self.scan_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)
        self.preview = QLabel()
        self.preview.setFixedSize(480, 320)
        self.preview.setStyleSheet('background-color: rgba(255,255,255,0.03); border-radius:8px;')
        self.preview.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview)
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

    def upload_image(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select Receipt Image', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if not path:
            return
        self.image_path = path
        pix = QPixmap(path).scaled(self.preview.width(), self.preview.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview.setPixmap(pix)

    def scan_receipt(self):
        if not self.image_path:
            QMessageBox.warning(self, 'No Image', 'Please upload a receipt image first.')
            return
        try:
            parsed = self.scanner.scan(self.image_path)
            txt = []
            txt.append(f"Merchant: {parsed.get('merchant')}")
            txt.append(f"Date: {parsed.get('date')}")
            txt.append(f"Total: {parsed.get('total')}")
            txt.append(f"Tax: {parsed.get('tax')}")
            txt.append(f"Payment: {parsed.get('payment_method')}")
            txt.append('\nItems:')
            for it in parsed.get('items', []):
                txt.append(f" - {it.get('name')} : {it.get('price')}")
            self.last_parsed = parsed
            self.result_area.setPlainText('\n'.join(txt))
        except Exception as e:
            QMessageBox.critical(self, 'Scan Error', f'Scan failed: {e}')

    def save_receipt(self):
        if not hasattr(self, 'last_parsed') or not self.last_parsed:
            QMessageBox.warning(self, 'Nothing to Save', 'Please scan a receipt first.')
            return
        p = self.last_parsed
        try:
            receipts_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'receipts')
            receipts_dir = os.path.abspath(receipts_dir)
            os.makedirs(receipts_dir, exist_ok=True)
            basename = os.path.basename(self.image_path) if self.image_path else f'receipt_{int(datetime.now().timestamp())}.png'
            safe_name = f"{int(datetime.now().timestamp())}_{basename}"
            dest = os.path.join(receipts_dir, safe_name)
            if self.image_path and os.path.exists(self.image_path):
                try:
                    shutil.copy2(self.image_path, dest)
                except Exception:
                    dest = self.image_path
            else:
                dest = self.image_path
            rid = self.repo.add_receipt(1, p.get('merchant'), p.get('date'), p.get('total') or 0.0, p.get('tax'), p.get('payment_method'), dest, p.get('ocr_text'))
            QMessageBox.information(self, 'Saved', f'Receipt saved with id {rid}')
            for cb in self.refresh_callbacks:
                cb()
        except Exception as e:
            QMessageBox.critical(self, 'Save Error', f'Failed to save receipt: {e}')
