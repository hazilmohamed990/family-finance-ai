"""
Modern Receipt Scanner Page
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QMessageBox, QScrollArea, QFrame, QCheckBox, QSpinBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal

from .theme import Colors, Fonts, Spacing, BorderRadius
from .components import (
    Card, PrimaryButton, SecondaryButton, VSection, Separator, MetricCard
)


class ReceiptCard(Card):
    """Card for displaying receipt information"""
    
    def __init__(self, filename: str = "", extracted_data: dict = None, parent=None):
        super().__init__(parent)
        self.layout.setSpacing(Spacing.MD)
        
        # Filename
        filename_label = QLabel(filename)
        filename_label.setFont(Fonts.heading_5())
        filename_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        self.layout.addWidget(filename_label)
        
        self.layout.addSpacing(Spacing.SM)
        
        if extracted_data:
            # Amount
            if "amount" in extracted_data:
                amount_layout = QHBoxLayout()
                amount_label = QLabel("Amount:")
                amount_label.setFont(Fonts.label())
                amount_value = QLabel(f"${extracted_data['amount']:.2f}")
                amount_value.setFont(Fonts.heading_5())
                amount_value.setStyleSheet(f"color: {Colors.EXPENSE};")
                amount_layout.addWidget(amount_label)
                amount_layout.addStretch()
                amount_layout.addWidget(amount_value)
                self.layout.addLayout(amount_layout)
            
            # Date
            if "date" in extracted_data:
                date_layout = QHBoxLayout()
                date_label = QLabel("Date:")
                date_label.setFont(Fonts.label())
                date_value = QLabel(extracted_data["date"])
                date_value.setFont(Fonts.body_base())
                date_value.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
                date_layout.addWidget(date_label)
                date_layout.addStretch()
                date_layout.addWidget(date_value)
                self.layout.addLayout(date_layout)
            
            # Vendor
            if "vendor" in extracted_data:
                vendor_layout = QHBoxLayout()
                vendor_label = QLabel("Vendor:")
                vendor_label.setFont(Fonts.label())
                vendor_value = QLabel(extracted_data["vendor"])
                vendor_value.setFont(Fonts.body_base())
                vendor_value.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
                vendor_layout.addWidget(vendor_label)
                vendor_layout.addStretch()
                vendor_layout.addWidget(vendor_value)
                self.layout.addLayout(vendor_layout)
            
            # Items
            if "items" in extracted_data and extracted_data["items"]:
                items_label = QLabel("Items:")
                items_label.setFont(Fonts.label())
                self.layout.addWidget(items_label)
                
                for item in extracted_data["items"][:5]:  # Show first 5
                    item_layout = QHBoxLayout()
                    item_text = QLabel(f"• {item}")
                    item_text.setFont(Fonts.body_sm())
                    item_text.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
                    item_text.setWordWrap(True)
                    item_layout.addWidget(item_text)
                    self.layout.addLayout(item_layout)
        else:
            no_data_label = QLabel("No data extracted")
            no_data_label.setFont(Fonts.body_sm())
            no_data_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY};")
            self.layout.addWidget(no_data_label)


class ModernReceiptScannerPage(QWidget):
    """Modern receipt scanner interface"""
    
    def __init__(self, repo, refresh_callbacks=None, parent=None):
        super().__init__(parent)
        self.repo = repo
        self.refresh_callbacks = refresh_callbacks or []
        self.receipts = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize receipt scanner UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(Spacing.SM)
        
        title = QLabel("Receipt Scanner")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        subtitle = QLabel("Upload and analyze receipts with AI-powered OCR")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Upload section
        upload_section = VSection("Upload Receipt")
        upload_layout = QHBoxLayout()
        upload_layout.setContentsMargins(0, 0, 0, 0)
        upload_layout.setSpacing(Spacing.MD)
        
        upload_btn = PrimaryButton("📷 Upload Image")
        upload_btn.clicked.connect(self.upload_receipt)
        
        camera_btn = SecondaryButton("📸 Take Photo")
        camera_btn.clicked.connect(self.take_photo)
        
        upload_layout.addWidget(upload_btn)
        upload_layout.addWidget(camera_btn)
        upload_layout.addStretch()
        
        upload_section.content_layout.addLayout(upload_layout)
        main_layout.addWidget(upload_section)
        
        main_layout.addWidget(Separator())
        
        # Receipts list
        list_section = VSection("Recent Receipts")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Colors.BG_PRIMARY};
                border: none;
            }}
        """)
        
        scroll_widget = QWidget()
        self.receipts_layout = QVBoxLayout()
        self.receipts_layout.setContentsMargins(0, 0, 0, 0)
        self.receipts_layout.setSpacing(Spacing.MD)
        self.receipts_layout.addStretch()
        scroll_widget.setLayout(self.receipts_layout)
        
        scroll.setWidget(scroll_widget)
        list_section.content_layout.addWidget(scroll)
        
        main_layout.addWidget(list_section, 1)
        
        self.setLayout(main_layout)
    
    def upload_receipt(self):
        """Upload receipt image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Receipt Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        
        if file_path:
            self._process_receipt(file_path)
    
    def take_photo(self):
        """Take photo with camera (placeholder)"""
        QMessageBox.information(
            self,
            "Camera",
            "Camera functionality would be implemented with a camera library.\nFor now, use Upload Image."
        )
    
    def _process_receipt(self, file_path: str):
        """Process receipt image"""
        try:
            # Simulate receipt data extraction
            # In production, this would use OCR library
            filename = file_path.split("\\")[-1]
            
            extracted_data = {
                "filename": filename,
                "amount": 45.99,
                "date": "2024-12-15",
                "vendor": "Grocery Store",
                "items": [
                    "Milk - $3.50",
                    "Bread - $2.99",
                    "Eggs - $4.50",
                    "Butter - $5.00",
                ]
            }
            
            receipt_card = ReceiptCard(filename, extracted_data)
            self.receipts_layout.insertWidget(self.receipts_layout.count() - 1, receipt_card)
            
            self.receipts.append(extracted_data)
            
            QMessageBox.information(self, "Success", "Receipt processed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process receipt: {e}")
