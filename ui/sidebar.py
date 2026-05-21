"""
Modern sidebar navigation component
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QFont
from .theme import Colors, Fonts, Spacing, BorderRadius
from .components import SidebarItem, Separator


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
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Logo
        logo_container = QWidget()
        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/images/logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
        
        logo_layout.addWidget(logo_label)
        logo_container.setLayout(logo_layout)
        logo_container.setFixedHeight(44)
        layout.addWidget(logo_container)
        
        layout.addSpacing(Spacing.MD)
        
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
        
        # Help
        help_label = QLabel("Help & Support")
        help_label.setFont(Fonts.caption())
        help_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY}; padding: 8px 12px;")
        layout.addWidget(help_label)
        
        help_btn = QPushButton("Documentation")
        help_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.SM}px;
                padding: 8px 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        help_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(help_btn)
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            ModernSidebar {{
                background-color: {Colors.BG_SECONDARY};
                border-right: 1px solid {Colors.BORDER_LIGHT};
            }}
        """)
        
        # Set initial active state
        self._update_active_item()
    
    def _on_item_clicked(self, page_idx: int):
        """Handle item click"""
        self.current_page = page_idx
        self._update_active_item()
        self.page_switched.emit(page_idx)
    
    def _update_active_item(self):
        """Update active item styling"""
        for i, item in enumerate(self.items):
            item.set_active(i == self.current_page)
    
    def set_current_page(self, page_idx: int):
        """Set current page"""
        self.current_page = page_idx
        self._update_active_item()
