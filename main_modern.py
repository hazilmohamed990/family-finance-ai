"""
Family Finance AI - Premium Desktop Application
Modern PyQt5 UI with fintech-grade styling
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

# Import new modern components
from ui.theme import GLOBAL_STYLESHEET, Colors, Fonts
from ui.sidebar import ModernSidebar
from ui.dashboard import DashboardPage
from ui.transactions import ModernExpensesPage, ModernIncomePage
from ui.ai_assistant import ModernAIAssistantPage
from ui.receipt_scanner import ModernReceiptScannerPage
from ui.settings import ModernSettingsPage

# Import data services
from ai.analyzer import FinanceAnalyzer
from core.data_service import DataService
from database.queries import FinanceRepository


class MainWindow(QMainWindow):
    """Main application window with modern fintech design"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Family Finance AI")
        self.setGeometry(0, 0, 1920, 1080)
        self.setMinimumSize(1200, 800)
        
        # Set window icon
        icon_path = "assets/images/logo.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize data layer
        self.repo = FinanceRepository()
        self.data_service = DataService(repo=self.repo)
        
        # Initialize pages
        self._init_pages()
        
        # Setup UI
        self._setup_ui()
        
        # Apply theme
        self._apply_theme()
    
    def _init_pages(self):
        """Initialize all application pages"""
        try:
            # Dashboard
            self.dashboard = DashboardPage(self.data_service)
            
            # AI Assistant (initialize first for callbacks)
            self.ai_assistant = ModernAIAssistantPage(self.repo)
            
            # Transactions with refresh callbacks
            refresh_callbacks = [self.dashboard.refresh, self.ai_assistant.load_ai_summary]
            self.expenses = ModernExpensesPage(self.repo, refresh_callbacks=refresh_callbacks)
            self.income = ModernIncomePage(self.repo, refresh_callback=self.ai_assistant.load_ai_summary)
            
            # Receipt scanner
            self.receipt_scanner = ModernReceiptScannerPage(self.repo, refresh_callbacks=refresh_callbacks)
            
            # Settings
            self.settings = ModernSettingsPage()
            
            # Store pages in order
            self.pages = [
                self.dashboard,
                self.expenses,
                self.income,
                self.ai_assistant,
                self.receipt_scanner,
                self.settings,
            ]
        except Exception as e:
            print(f"Error initializing pages: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _setup_ui(self):
        """Setup main UI layout"""
        try:
            # Central widget
            central_widget = QWidget()
            main_layout = QHBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)
            
            # Sidebar
            self.sidebar = ModernSidebar()
            self.sidebar.setFixedWidth(200)
            self.sidebar.page_switched.connect(self._switch_page)
            
            # Stack widget for pages
            self.stack = QStackedWidget()
            for page in self.pages:
                self.stack.addWidget(page)
            
            # Add to layout
            main_layout.addWidget(self.sidebar)
            main_layout.addWidget(self.stack, 1)
            
            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)
        except Exception as e:
            print(f"Error setting up UI: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _switch_page(self, page_index: int):
        """Switch to page"""
        self.stack.setCurrentIndex(page_index)
    
    def _apply_theme(self):
        """Apply global theme stylesheet"""
        self.setStyleSheet(GLOBAL_STYLESHEET)


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Apply global font
    app.setFont(Fonts.body_base())
    
    try:
        # Create and show main window
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
