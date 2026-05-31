"""
Receipt Scanner - Upload/capture receipts and extract expense data
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QFrame, QProgressBar, QTableWidget, QTableWidgetItem, QTabWidget,
    QListWidget, QListWidgetItem, QMessageBox, QLineEdit, QDateEdit,
    QDoubleSpinBox, QComboBox, QFormLayout, QDialog
)
from PyQt5.QtCore import Qt, QSize, QDate, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap, QImage
from PyQt5.QtChart import QChart, QChartView, QPieSeries

import os
from datetime import datetime
from pathlib import Path

from database.enhanced_db import EnhancedDatabase
from ui.theme import Colors, Fonts, Spacing, BorderRadius
from .camera_dialog import CameraCaptureDialog


class ReceiptPreviewCard(QFrame):
    """Display receipt preview"""
    
    def __init__(self, receipt_path: str, merchant: str = "", amount: str = "", 
                 date: str = "", parent=None):
        super().__init__(parent)
        self.receipt_path = receipt_path
        self.merchant = merchant
        self.amount = amount
        self.date = date
        self.init_ui()
    
    def init_ui(self):
        """Initialize preview card"""
        layout = QVBoxLayout()
        layout.setContentsMargins(Spacing.MD, Spacing.MD, Spacing.MD, Spacing.MD)
        layout.setSpacing(Spacing.SM)
        
        # Image preview
        if os.path.exists(self.receipt_path):
            pixmap = QPixmap(self.receipt_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(150, Qt.SmoothTransformation)
                img_label = QLabel()
                img_label.setPixmap(pixmap)
                img_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(img_label)
        
        # Details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(Spacing.XS)
        
        merchant_label = QLabel(self.merchant or "Unknown Merchant")
        merchant_label.setFont(Fonts.body_sm())
        merchant_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: bold;")
        
        amount_label = QLabel(self.amount or "$ 0.00")
        amount_label.setFont(Fonts.body_base())
        amount_label.setStyleSheet(f"color: {Colors.EXPENSE}; font-weight: bold;")
        
        date_label = QLabel(self.date or "Unknown Date")
        date_label.setFont(Fonts.caption())
        date_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        details_layout.addWidget(merchant_label)
        details_layout.addWidget(amount_label)
        details_layout.addWidget(date_label)
        
        layout.addLayout(details_layout)
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
        """)


class ReceiptScanner(QWidget):
    """Receipt scanning and OCR interface"""
    
    receipt_processed = pyqtSignal(dict)
    
    def __init__(self, db: EnhancedDatabase, parent_id: int, parent=None):
        super().__init__(parent)
        self.db = db
        self.parent_id = parent_id
        self.current_receipt = None
        self.receipts = []
        self.init_ui()
        self.load_receipts()
    
    def init_ui(self):
        """Initialize scanner UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(Spacing.SM)
        
        title = QLabel("📸 Receipt Scanner")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        subtitle = QLabel("Upload receipts and extract expense data automatically")
        subtitle.setFont(Fonts.body_sm())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
            QTabBar::tab {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                padding: {Spacing.MD}px;
                margin-right: {Spacing.SM}px;
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.ACCENT};
                color: white;
            }}
        """)
        
        # Upload tab
        upload_widget = self.create_upload_tab()
        tabs.addTab(upload_widget, "📤 Upload Receipt")
        
        # History tab
        history_widget = self.create_history_tab()
        tabs.addTab(history_widget, "📋 Receipt History")
        
        main_layout.addWidget(tabs)
        
        self.setLayout(main_layout)
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
    
    def create_upload_tab(self) -> QWidget:
        """Create upload receipt tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.LG)
        
        # Upload area
        upload_frame = QFrame()
        upload_layout = QVBoxLayout()
        upload_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        upload_layout.setSpacing(Spacing.LG)
        upload_layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        icon_label = QLabel("📸")
        icon_label.setFont(QFont("Arial", 64))
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Text
        text_label = QLabel("Drop receipt image or click to upload")
        text_label.setFont(Fonts.heading_4())
        text_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        text_label.setAlignment(Qt.AlignCenter)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Spacing.LG)
        button_layout.setAlignment(Qt.AlignCenter)
        
        upload_btn = QPushButton("📁 Choose Image")
        upload_btn.setMinimumHeight(48)
        upload_btn.setMinimumWidth(200)
        upload_btn.setFont(Fonts.body_base())
        upload_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT_HOVER};
            }}
        """)
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.clicked.connect(self.select_receipt_image)
        
        camera_btn = QPushButton("📷 Take Photo")
        camera_btn.setMinimumHeight(48)
        camera_btn.setMinimumWidth(200)
        camera_btn.setFont(Fonts.body_base())
        camera_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        camera_btn.setCursor(Qt.PointingHandCursor)
        camera_btn.clicked.connect(lambda: CameraCaptureDialog(self.process_receipt).exec_())  # Open live camera capture and process image
        
        button_layout.addWidget(upload_btn)
        button_layout.addWidget(camera_btn)
        
        upload_layout.addWidget(icon_label)
        upload_layout.addWidget(text_label)
        upload_layout.addLayout(button_layout)
        
        upload_frame.setLayout(upload_layout)
        upload_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px dashed {Colors.BORDER_MEDIUM};
                border-radius: {BorderRadius.LG}px;
            }}
        """)
        
        layout.addWidget(upload_frame)
        
        # Preview section
        self.preview_container = QVBoxLayout()
        self.preview_container.setSpacing(Spacing.LG)
        layout.addLayout(self.preview_container)
        
        # Extract details section
        self.extract_container = QVBoxLayout()
        self.extract_container.setSpacing(Spacing.MD)
        layout.addLayout(self.extract_container)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_history_tab(self) -> QWidget:
        """Create receipt history tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.LG)
        
        # List of receipts
        self.receipt_list = QListWidget()
        self.receipt_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
            QListWidget::item {{
                padding: {Spacing.MD}px;
                border-bottom: 1px solid {Colors.BORDER_LIGHT};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.HOVER};
            }}
        """)
        self.receipt_list.itemClicked.connect(self.on_receipt_selected)
        
        layout.addWidget(QLabel("Recent Receipts"))
        layout.addWidget(self.receipt_list)
        
        # Details pane
        details_frame = QFrame()
        details_layout = QVBoxLayout()
        
        details_title = QLabel("Details")
        details_title.setFont(Fonts.heading_4())
        
        self.details_text = QLineEdit()
        self.details_text.setReadOnly(True)
        
        details_layout.addWidget(details_title)
        details_layout.addWidget(self.details_text)
        
        details_frame.setLayout(details_layout)
        layout.addWidget(details_frame)
        
        widget.setLayout(layout)
        return widget
    
    def select_receipt_image(self):
        """Select receipt image file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Receipt Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        if file_path and os.path.exists(file_path):
            self.process_receipt(file_path)
    
    def process_receipt(self, file_path: str):
        """Process receipt image"""
        # Copy image to assets
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "receipts")
        os.makedirs(assets_dir, exist_ok=True)
        
        # Generate unique filename
        filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        dest_path = os.path.join(assets_dir, filename)
        
        # Copy file
        import shutil
        shutil.copy(file_path, dest_path)
        
        # Mock OCR extraction (would use pytesseract in production)
        merchant = "Sample Store"
        amount = 45.99
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Show preview
        self.show_receipt_preview(dest_path, merchant, amount, date)
        
        # Save to database
        receipt_id = self.db.add_receipt(
            self.parent_id,
            merchant,
            amount,
            date,
            image_path=dest_path
        )
        
        # Show extraction form
        self.show_extraction_form(receipt_id, merchant, amount, date)
    
    def show_receipt_preview(self, receipt_path: str, merchant: str, amount: float, date: str):
        """Show receipt preview"""
        # Clear existing preview
        while self.preview_container.count():
            item = self.preview_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        preview_card = ReceiptPreviewCard(
            receipt_path,
            merchant,
            f"${amount:.2f}",
            date
        )
        self.preview_container.addWidget(preview_card)
    
    def show_extraction_form(self, receipt_id: int, merchant: str, amount: float, date: str):
        """Show expense extraction form"""
        # Clear existing form
        while self.extract_container.count():
            item = self.extract_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        form_frame = QFrame()
        form_layout = QFormLayout()
        form_layout.setSpacing(Spacing.MD)
        
        title = QLabel("Confirm and Save Expense")
        title.setFont(Fonts.heading_4())
        form_layout.addRow(title)
        
        # Merchant
        merchant_input = QLineEdit(merchant)
        form_layout.addRow(QLabel("Merchant:"), merchant_input)
        
        # Amount
        amount_input = QDoubleSpinBox()
        amount_input.setValue(amount)
        amount_input.setMinimum(0)
        amount_input.setMaximum(10000)
        amount_input.setDecimals(2)
        form_layout.addRow(QLabel("Amount:"), amount_input)
        
        # Date
        date_input = QDateEdit()
        date_input.setDate(QDate.fromString(date, "yyyy-MM-dd"))
        form_layout.addRow(QLabel("Date:"), date_input)
        
        # Category
        category_combo = QComboBox()
        category_combo.addItems([
            "Groceries",
            "Utilities",
            "Transport",
            "Entertainment",
            "Health",
            "Other"
        ])
        form_layout.addRow(QLabel("Category:"), category_combo)
        
        # Description
        desc_input = QLineEdit()
        desc_input.setPlaceholderText("Optional description")
        form_layout.addRow(QLabel("Description:"), desc_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("✓ Save Expense")
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.SUCCESS};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(lambda: self.save_expense(
            merchant_input.text(),
            amount_input.value(),
            date_input.date().toString("yyyy-MM-dd"),
            category_combo.currentText(),
            desc_input.text(),
            receipt_id
        ))
        
        cancel_btn = QPushButton("✕ Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
        """)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.clear_extraction_form)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        form_layout.addRow(button_layout)
        
        form_frame.setLayout(form_layout)
        form_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.LG}px;
            }}
        """)
        
        self.extract_container.addWidget(form_frame)
    
    def save_expense(self, merchant: str, amount: float, date: str, 
                    category: str, description: str, receipt_id: int):
        """Save extracted expense"""
        self.db.add_parent_expense(
            self.parent_id,
            category,
            amount,
            description or merchant,
            date,
            receipt_id
        )
        
        QMessageBox.information(self, "Success", f"Expense saved: {merchant} - ${amount:.2f}")
        self.clear_extraction_form()
        self.load_receipts()
    
    def clear_extraction_form(self):
        """Clear extraction form"""
        while self.extract_container.count():
            item = self.extract_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def load_receipts(self):
        """Load receipt history"""
        self.receipts = self.db.get_receipts(self.parent_id)
        
        self.receipt_list.clear()
        for receipt in self.receipts:
            item_text = f"{receipt['merchant']} - ${receipt['amount']:.2f} ({receipt['date']})"
            item = QListWidgetItem(item_text)
            self.receipt_list.addItem(item)
    
    def on_receipt_selected(self, item: QListWidgetItem):
        """Handle receipt selection"""
        index = self.receipt_list.row(item)
        if 0 <= index < len(self.receipts):
            receipt = self.receipts[index]
            details = f"Merchant: {receipt['merchant']}\nAmount: ${receipt['amount']:.2f}\nDate: {receipt['date']}\nCategory: {receipt.get('category', 'N/A')}"
            self.details_text.setText(details)
