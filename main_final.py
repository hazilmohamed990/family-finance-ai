"""
Family Finance AI - Production Ready
Premium Apple-Inspired Fintech Desktop Application
Global SF Pro Font with Green + White Theme
"""

import sys
import os
import warnings
warnings.filterwarnings("ignore")

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QLabel, QPushButton, QMessageBox, QScrollArea,
    QFrame
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QRect
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap, QBrush, QPainter
from PyQt5.QtCore import QObject

import sqlite3
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import theme with SF Pro font management
from ui.theme import (
    Colors, Fonts, Spacing, BorderRadius, Shadows, 
    GLOBAL_STYLESHEET, FontManager
)

# Import UI components
from ui.components import Card, StatCard
from database.enhanced_db import EnhancedDatabase

class signals(QObject):
    """Global signals for app-wide communication"""
    page_switched = pyqtSignal(int)
    user_logged_in = pyqtSignal(dict)


class BackgroundWidget(QWidget):
    """Widget that supports background image with overlay"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_pixmap = None
        self.load_background()
    
    def load_background(self):
        """Load and cache background image"""
        bg_path = "assets/images/background.png"
        if os.path.exists(bg_path):
            self.background_pixmap = QPixmap(bg_path)
    
    def paintEvent(self, event):
        """Paint background with elegant overlay"""
        if self.background_pixmap and not self.background_pixmap.isNull():
            painter = QPainter(self)
            
            # Draw scaled background
            scaled_pixmap = self.background_pixmap.scaledToWidth(
                self.width(), Qt.SmoothTransformation
            )
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
            
            # Draw subtle overlay for better text readability
            overlay_color = QColor(255, 255, 255, 160)  # Soft white overlay
            painter.fillRect(self.rect(), overlay_color)
        else:
            # Fallback solid background
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(Colors.BG_PRIMARY))
        
        painter.end()


class MacOSWindowControls(QFrame):
    """macOS-style window control buttons"""
    
    close_clicked = pyqtSignal()
    minimize_clicked = pyqtSignal()
    maximize_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(28)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: none;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 4, 12, 4)
        layout.setSpacing(8)
        
        # Close button (red)
        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(12, 12)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #FF5F56;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #FF6B63;
            }}
        """)
        self.close_btn.clicked.connect(self.close_clicked.emit)
        
        # Minimize button (yellow)
        self.minimize_btn = QPushButton()
        self.minimize_btn.setFixedSize(12, 12)
        self.minimize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFBD2E;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #FFCA3A;
            }}
        """)
        self.minimize_btn.clicked.connect(self.minimize_clicked.emit)
        
        # Maximize button (green)
        self.maximize_btn = QPushButton()
        self.maximize_btn.setFixedSize(12, 12)
        self.maximize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT_HOVER};
            }}
        """)
        self.maximize_btn.clicked.connect(self.maximize_clicked.emit)
        
        layout.addWidget(self.close_btn)
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.maximize_btn)
        layout.addStretch()
        
        self.setLayout(layout)


class TitleBar(QFrame):
    """Premium custom titlebar with dragging support"""
    
    def __init__(self, title="Family Finance AI", parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border-bottom: 1px solid {Colors.BORDER_LIGHT};
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(0)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(Fonts.heading_5())
        title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        layout.addWidget(title_label)
        layout.addStretch()
        
        # Window controls
        self.controls = MacOSWindowControls()
        layout.addWidget(self.controls)
        
        self.setLayout(layout)
        self.drag_position = None
    
    def mousePressEvent(self, event):
        """Record position for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.window().frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.window().move(event.globalPos() - self.drag_position)


class MainWindow(QMainWindow):
    """Main application window with complete UI"""
    
    def __init__(self):
        super().__init__()
        # Frameless window for custom macOS-style titlebar and controls
        self.setWindowFlags(Qt.FramelessWindowHint)
        try:
            self.setAttribute(Qt.WA_TranslucentBackground, True)
        except Exception:
            pass
        self.setWindowTitle("Family Finance AI")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize database
        self.db = EnhancedDatabase("finance.db")
        
        # Apply global SF Pro font
        self._apply_global_font()
        
        # Apply stylesheet
        self.setStyleSheet(GLOBAL_STYLESHEET)
        
        self.init_ui()
    
    def _apply_global_font(self):
        """Force SF Pro font globally across the entire application"""
        # Load SF Pro font first
        FontManager.load_font()
        
        # Create and apply global font
        global_font = QFont("SF Pro", 11, QFont.Normal)
        global_font.setStyleStrategy(QFont.PreferAntialias)
        
        app = QApplication.instance()
        app.setFont(global_font)
    
    def init_ui(self):
        """Initialize main UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom titlebar
        titlebar = TitleBar()
        titlebar.controls.close_clicked.connect(self.close)
        titlebar.controls.minimize_clicked.connect(self.showMinimized)
        titlebar.controls.maximize_clicked.connect(self.toggle_maximize)
        main_layout.addWidget(titlebar)
        
        # Main content area with background
        content_frame = QFrame()
        content_frame.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self._create_sidebar()
        content_layout.addWidget(self.sidebar)
        
        # Main content area
        self.pages = QStackedWidget()
        self.pages.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        
        # Create pages
        self.dashboard_page = self._create_dashboard()
        self.pages.addWidget(self.dashboard_page)
        
        content_layout.addWidget(self.pages, 1)
        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame, 1)
        
        central_widget.setLayout(main_layout)
    
    def _create_sidebar(self):
        """Create modern sidebar"""
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border-right: 1px solid {Colors.BORDER_LIGHT};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(12)
        
        # Logo area
        logo_container = QFrame()
        logo_layout = QVBoxLayout()
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        logo_label = QLabel()
        logo_path = "assets/images/logo.png"
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_pixmap = logo_pixmap.scaledToWidth(80, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
        
        app_name = QLabel("Family Finance")
        app_name.setFont(Fonts.heading_4())
        app_name.setStyleSheet(f"color: {Colors.ACCENT}; padding-top: 12px;")
        app_name.setAlignment(Qt.AlignCenter)
        
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(app_name)
        logo_container.setLayout(logo_layout)
        layout.addWidget(logo_container)
        
        layout.addSpacing(24)
        
        # Navigation items
        nav_items = [
            ("Dashboard", 0),
            ("Expenses", 1),
            ("Income", 2),
            ("Analytics", 3),
            ("Settings", 4)
        ]
        
        for name, idx in nav_items:
            btn = QPushButton(name)
            btn.setMinimumHeight(44)
            btn.setFont(Fonts.body_base())
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.BG_TERTIARY};
                    color: {Colors.TEXT_PRIMARY};
                    border: 1px solid {Colors.BORDER_LIGHT};
                    border-radius: {BorderRadius.MD}px;
                    padding: 0px 16px;
                    text-align: left;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {Colors.HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {Colors.ACCENT};
                    color: white;
                }}
            """)
            btn.clicked.connect(lambda checked, i=idx: self.pages.setCurrentIndex(i))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        sidebar.setLayout(layout)
        return sidebar
    
    def _create_dashboard(self):
        """Create dashboard page"""
        dashboard = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        layout.setSpacing(Spacing.XXL)
        
        # Header
        header = QLabel("Dashboard")
        header.setFont(Fonts.heading_2())
        header.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(header)
        
        subtitle = QLabel("Financial Overview & Insights")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(subtitle)
        
        # Summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(Spacing.LG)
        
        cards = [
            ("Total Income", "$0.00", Colors.INCOME),
            ("Total Expenses", "$0.00", Colors.EXPENSE),
            ("Net Savings", "$0.00", Colors.ACCENT),
            ("Savings Rate", "0%", Colors.SUCCESS)
        ]
        
        for title, value, color in cards:
            card = StatCard(title, value)
            card.value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: 700;")
            cards_layout.addWidget(card)
        
        layout.addLayout(cards_layout)
        layout.addStretch()
        
        dashboard.setLayout(layout)
        return dashboard
    
    def toggle_maximize(self):
        """Toggle window maximize"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Set application-wide font to SF Pro before creating any widgets
    FontManager.load_font()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
