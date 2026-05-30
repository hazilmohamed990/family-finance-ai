"""
Modern sidebar navigation component
Premium Apple-inspired with green + white theme
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QFont, QCursor
from .theme import Colors, Fonts, Spacing, BorderRadius
from .components import SidebarItem, Separator, PrimaryButton, GhostButton


class ModernSidebar(QWidget):
    """Floating modern sidebar with icon navigation"""
    
    page_switched = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 0
        self.items = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize sidebar UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(12)
        
        # Logo container with enhanced styling
        logo_container = QFrame()
        logo_container.setStyleSheet("background-color: transparent; border: none;")
        logo_layout = QVBoxLayout()
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(8)
        
        # Logo image - increased size
        logo_label = QLabel()
        logo_path = "assets/images/logo.png"
        try:
            import os
            if os.path.exists(logo_path):
                logo_pixmap = QPixmap(logo_path)
                if not logo_pixmap.isNull():
                    # Significantly larger logo
                    logo_pixmap = logo_pixmap.scaledToWidth(
                        100, Qt.SmoothTransformation
                    )
                    logo_label.setPixmap(logo_pixmap)
                    logo_label.setAlignment(Qt.AlignCenter)
        except:
            pass
        
        # App name
        app_name = QLabel("Family Finance")
        app_name.setFont(Fonts.heading_4())
        app_name.setStyleSheet(f"""
            color: {Colors.ACCENT};
            font-weight: 700;
            padding-top: 8px;
        """)
        app_name.setAlignment(Qt.AlignCenter)
        
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(app_name)
        logo_container.setLayout(logo_layout)
        layout.addWidget(logo_container)
        
        layout.addSpacing(Spacing.LG)
        
        # Navigation items
        nav_pages = [
            ("Dashboard", "assets/icons/dashboard.png", 0),
            ("Expenses", "assets/icons/expenses.png", 1),
            ("Income", "assets/icons/income.png", 2),
            ("AI Assistant", "assets/icons/ai.png", 3),
            ("Receipts", "assets/icons/receipts.png", 4),
        ]
        
        for i, (name, icon_path, page_idx) in enumerate(nav_pages):
            item = SidebarItem(name, icon_path)
            item.clicked.connect(lambda checked, idx=page_idx: self._on_item_clicked(idx))
            self.items.append(item)
            layout.addWidget(item)
        
        layout.addSpacing(Spacing.MD)
        layout.addWidget(Separator())
        layout.addSpacing(Spacing.MD)
        
        # Settings item
        settings_item = SidebarItem("Settings", "assets/icons/settings.png")
        settings_item.clicked.connect(lambda: self._on_item_clicked(5))
        self.items.append(settings_item)
        layout.addWidget(settings_item)
        
        layout.addStretch()
        
        # Help text at bottom
        help_label = QLabel("Need Help?")
        help_label.setFont(Fonts.caption())
        help_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY}; padding: 8px 0px;")
        help_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(help_label)
        
        help_text = QLabel("View documentation or contact support")
        help_text.setFont(Fonts.body_xs())
        help_text.setStyleSheet(f"""
            color: {Colors.TEXT_TERTIARY};
            text-align: center;
        """)
        help_text.setWordWrap(True)
        help_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(help_text)
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            ModernSidebar {{
                background-color: {Colors.BG_SECONDARY};
                border-right: 1px solid {Colors.BORDER_LIGHT};
            }}
        """)
    
    def _on_item_clicked(self, page_idx):
        """Handle item click"""
        self.current_page = page_idx
        self.page_switched.emit(page_idx)
        
        # Update visual state
        for item in self.items:
            item.setProperty("active", False)
        
        if page_idx < len(self.items):
            self.items[page_idx].setProperty("active", True)
