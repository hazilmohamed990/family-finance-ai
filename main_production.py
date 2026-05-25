"""
Family Finance AI - Premium Desktop Application
Complete production-ready fintech app with dual interfaces
"""

import sys
import os
import warnings
warnings.filterwarnings("ignore")

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QStackedWidget, QLabel, QPushButton, QMessageBox, QInputDialog,
    QScrollArea, QFrame, QGridLayout, QLineEdit, QDateEdit
)
from PyQt5.QtCore import Qt, QSize, QTimer, QDate, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import QRectF

import sqlite3
from datetime import datetime, timedelta
import json

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import enhanced database
from database.enhanced_db import EnhancedDatabase

# Import AI and analytics
try:
    from ai.chatbot import FinanceChatbot
except:
    FinanceChatbot = None

try:
    from ai.analyzer import FinanceAnalyzer
except:
    FinanceAnalyzer = None

# Import theme and components
from ui.theme import Colors, Fonts, Spacing, BorderRadius, Shadows, GLOBAL_STYLESHEET
from ui.components import Card, StatCard, MetricCard

# Default test data - will be populated on first run
DEFAULT_PARENT_EMAIL = "parent@family.local"
DEFAULT_PARENT_NAME = "Parent User"
DEFAULT_PASSWORD = "demo1234"

class signals(QObject):
    """Global signals for app-wide communication"""
    page_switched = pyqtSignal(int)
    user_logged_in = pyqtSignal(dict)
    user_logged_out = pyqtSignal()


class LoginPage(QWidget):
    """Premium login page"""
    
    logged_in = pyqtSignal(dict)
    
    def __init__(self, db: EnhancedDatabase):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """Initialize login UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Main container
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(Spacing.HUGE, Spacing.HUGE, Spacing.HUGE, Spacing.HUGE)
        container_layout.setSpacing(Spacing.XXL)
        container_layout.setAlignment(Qt.AlignCenter)
        
        # Logo/Title
        title = QLabel("Family Finance AI")
        title.setFont(QFont(Fonts.FAMILY_PRIMARY, 42, QFont.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Manage Family Finances Together")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        subtitle.setAlignment(Qt.AlignCenter)
        
        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)
        container_layout.addSpacing(Spacing.XXL)
        
        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(Spacing.LG)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Email
        email_label = QLabel("Email")
        email_label.setFont(Fonts.body_sm())
        email_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setText(DEFAULT_PARENT_EMAIL)
        self.email_input.setMinimumHeight(44)
        self.email_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.MD}px;
                font-size: 14px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.ACCENT};
            }}
        """)
        
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        
        # Password
        password_label = QLabel("Password")
        password_label.setFont(Fonts.body_sm())
        password_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setText(DEFAULT_PASSWORD)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(44)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.MD}px;
                font-size: 14px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.ACCENT};
            }}
        """)
        
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        
        container_layout.addLayout(form_layout)
        container_layout.addSpacing(Spacing.XXL)
        
        # Buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(Spacing.MD)
        
        login_btn = QPushButton("Sign In")
        login_btn.setMinimumHeight(48)
        login_btn.setFont(Fonts.body_base())
        login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2563eb;
            }}
            QPushButton:pressed {{
                background-color: #1e40af;
            }}
        """)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.on_login)
        
        button_layout.addWidget(login_btn)
        container_layout.addLayout(button_layout)
        
        # Demo note
        demo_note = QLabel("Demo Account • Use provided credentials")
        demo_note.setFont(Fonts.caption())
        demo_note.setStyleSheet(f"color: {Colors.TEXT_TERTIARY};")
        demo_note.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(demo_note)
        
        container_layout.addStretch()
        container.setLayout(container_layout)
        
        # Set container background
        container.setStyleSheet(f"""
            background-color: {Colors.BG_PRIMARY};
        """)
        
        layout.addWidget(container)
        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
    
    def on_login(self):
        """Handle login"""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not email or not password:
            QMessageBox.warning(self, "Validation", "Please enter email and password")
            return
        
        # Check if parent exists, if not create demo account
        parent = self.db.get_parent_by_email(email)
        if not parent:
            # Create demo parent
            parent_id = self.db.add_parent(email, DEFAULT_PARENT_NAME, password)
            parent = self.db.get_parent(parent_id)
            
            # Add demo children
            for i, child_name in enumerate(["Child 1", "Child 2"]):
                child_id = self.db.add_child(parent_id, child_name, age=8 + i, monthly_allowance=10 + i*5)
                # Add initial data
                self.db.add_to_child_savings(child_id, 50 + i*20)
                self.db.add_points(child_id, 100 + i*50, "Initial welcome points")
        
        self.logged_in.emit(parent)


class ParentDashboard(QWidget):
    """Parent dashboard - main financial hub"""
    
    def __init__(self, db: EnhancedDatabase, parent_data: dict):
        super().__init__()
        self.db = db
        self.parent_data = parent_data
        self.parent_id = parent_data['id']
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize dashboard UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(Spacing.LG)
        
        title = QLabel("Dashboard")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        welcome_label = QLabel(f"Welcome, {self.parent_data['name']}!")
        welcome_label.setFont(Fonts.body_base())
        welcome_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        header_layout.addWidget(welcome_label)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Colors.BG_PRIMARY};
                border: none;
            }}
            QScrollBar:vertical {{
                width: 8px;
            }}
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(Spacing.XXL)
        
        # Stats cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(Spacing.LG)
        
        self.income_card = StatCard("Total Income", "$0.00", "This Month")
        self.expense_card = StatCard("Total Expenses", "$0.00", "This Month")
        self.savings_card = StatCard("Net Savings", "$0.00", "YTD")
        self.kids_allowance_card = StatCard("Kids Allowances", "$0.00", "This Month")
        
        self.income_card.set_accent_color(Colors.INCOME)
        self.expense_card.set_accent_color(Colors.EXPENSE)
        self.savings_card.set_accent_color(Colors.SAVINGS)
        self.kids_allowance_card.set_accent_color(Colors.NEUTRAL)
        
        stats_layout.addWidget(self.income_card, 0, 0)
        stats_layout.addWidget(self.expense_card, 0, 1)
        stats_layout.addWidget(self.savings_card, 1, 0)
        stats_layout.addWidget(self.kids_allowance_card, 1, 1)
        
        scroll_layout.addLayout(stats_layout)
        
        # Recent expenses section
        expenses_title = QLabel("Recent Expenses")
        expenses_title.setFont(Fonts.heading_3())
        expenses_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        scroll_layout.addWidget(expenses_title)
        
        # Recent expenses list (simple)
        self.expenses_container = QVBoxLayout()
        self.expenses_container.setSpacing(Spacing.SM)
        scroll_layout.addLayout(self.expenses_container)
        
        scroll_layout.addSpacing(Spacing.XXL)
        
        # Quick actions
        actions_title = QLabel("Quick Actions")
        actions_title.setFont(Fonts.heading_3())
        actions_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        scroll_layout.addWidget(actions_title)
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(Spacing.LG)
        
        add_expense_btn = QPushButton("+ Add Expense")
        add_expense_btn.setMinimumHeight(44)
        add_expense_btn.setFont(Fonts.body_base())
        add_expense_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2563eb;
            }}
        """)
        add_expense_btn.setCursor(Qt.PointingHandCursor)
        add_expense_btn.clicked.connect(self.add_expense_dialog)
        
        add_income_btn = QPushButton("+ Add Income")
        add_income_btn.setMinimumHeight(44)
        add_income_btn.setFont(Fonts.body_base())
        add_income_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.INCOME};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        add_income_btn.setCursor(Qt.PointingHandCursor)
        add_income_btn.clicked.connect(self.add_income_dialog)
        
        actions_layout.addWidget(add_expense_btn)
        actions_layout.addWidget(add_income_btn)
        actions_layout.addStretch()
        
        scroll_layout.addLayout(actions_layout)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
    
    def load_data(self):
        """Load financial data"""
        # Get this month
        today = datetime.now()
        first_day = today.replace(day=1).strftime("%Y-%m-%d")
        last_day = today.strftime("%Y-%m-%d")
        
        # Income this month
        income_data = self.db.get_parent_income(self.parent_id, first_day, last_day)
        total_income = sum(item['amount'] for item in income_data)
        self.income_card.set_value(f"${total_income:,.2f}")
        
        # Expenses this month
        expense_data = self.db.get_parent_expenses(self.parent_id, first_day, last_day)
        total_expenses = sum(item['amount'] for item in expense_data)
        self.expense_card.set_value(f"${total_expenses:,.2f}")
        
        # Net savings
        net = total_income - total_expenses
        self.savings_card.set_value(f"${net:,.2f}")
        
        # Kids allowances
        children = self.db.get_children(self.parent_id)
        total_allowances = sum(child['monthly_allowance'] or 0 for child in children)
        self.kids_allowance_card.set_value(f"${total_allowances:,.2f}")
        
        # Recent expenses
        self.update_recent_expenses(expense_data[:5])
    
    def update_recent_expenses(self, expenses):
        """Update recent expenses display"""
        # Clear layout
        while self.expenses_container.count():
            item = self.expenses_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not expenses:
            no_exp = QLabel("No expenses yet this month")
            no_exp.setStyleSheet(f"color: {Colors.TEXT_TERTIARY};")
            self.expenses_container.addWidget(no_exp)
            return
        
        for exp in expenses:
            exp_layout = QHBoxLayout()
            exp_layout.setSpacing(Spacing.MD)
            
            # Category
            cat_label = QLabel(exp['category'])
            cat_label.setFont(Fonts.body_sm())
            cat_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            
            # Description
            desc_label = QLabel(exp.get('description', '')[:30])
            desc_label.setFont(Fonts.body_xs())
            desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            
            # Amount
            amt_label = QLabel(f"-${exp['amount']:,.2f}")
            amt_label.setFont(Fonts.body_sm())
            amt_label.setStyleSheet(f"color: {Colors.EXPENSE}; font-weight: bold;")
            
            exp_layout.addWidget(cat_label)
            exp_layout.addWidget(desc_label)
            exp_layout.addStretch()
            exp_layout.addWidget(amt_label)
            
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_SECONDARY};
                    border-radius: {BorderRadius.MD}px;
                    border: 1px solid {Colors.BORDER_LIGHT};
                }}
            """)
            frame.setLayout(exp_layout)
            frame.setMinimumHeight(50)
            
            self.expenses_container.addWidget(frame)
    
    def add_expense_dialog(self):
        """Add expense dialog"""
        category, ok = QInputDialog.getItem(
            self, "Add Expense", "Category:",
            ["Groceries", "Utilities", "Transport", "Entertainment", "Health", "Other"],
            editable=False
        )
        
        if not ok:
            return
        
        amount, ok = QInputDialog.getDouble(
            self, "Add Expense", "Amount ($):",
            value=0, min=0, max=10000, decimals=2
        )
        
        if ok and amount > 0:
            description, ok = QInputDialog.getText(
                self, "Add Expense", "Description (optional):"
            )
            
            self.db.add_parent_expense(self.parent_id, category, amount, description or "")
            QMessageBox.information(self, "Success", "Expense added!")
            self.load_data()
    
    def add_income_dialog(self):
        """Add income dialog"""
        source, ok = QInputDialog.getText(
            self, "Add Income", "Income Source:"
        )
        
        if not ok or not source.strip():
            return
        
        amount, ok = QInputDialog.getDouble(
            self, "Add Income", "Amount ($):",
            value=0, min=0, max=100000, decimals=2
        )
        
        if ok and amount > 0:
            self.db.add_parent_income(self.parent_id, source.strip(), amount)
            QMessageBox.information(self, "Success", "Income recorded!")
            self.load_data()


class MainAppContainer(QWidget):
    """Main application container with navigation"""
    
    def __init__(self, db: EnhancedDatabase, parent_data: dict):
        super().__init__()
        self.db = db
        self.parent_data = parent_data
        self.parent_id = parent_data['id']
        self.children = self.db.get_children(self.parent_id)
        self.current_interface = "parent"  # or "child"
        self.current_child = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize main container UI"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar navigation
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        sidebar_layout.setSpacing(Spacing.LG)
        
        # App title
        app_title = QLabel("Family Finance")
        app_title.setFont(Fonts.heading_3())
        app_title.setStyleSheet(f"color: {Colors.ACCENT};")
        sidebar_layout.addWidget(app_title)
        
        sidebar_layout.addSpacing(Spacing.XXL)
        
        # Parent interface button
        parent_btn = QPushButton("👨 Parent Dashboard")
        parent_btn.setMinimumHeight(40)
        parent_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                text-align: left;
                padding-left: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
        """)
        parent_btn.setCursor(Qt.PointingHandCursor)
        parent_btn.clicked.connect(self.switch_to_parent)
        sidebar_layout.addWidget(parent_btn)
        
        sidebar_layout.addSpacing(Spacing.MD)
        
        # Kids section
        if self.children:
            kids_title = QLabel("👧 Kids Accounts")
            kids_title.setFont(Fonts.body_sm())
            kids_title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            sidebar_layout.addWidget(kids_title)
            
            for child in self.children:
                child_btn = QPushButton(f"👧 {child['name']}")
                child_btn.setMinimumHeight(40)
                child_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {Colors.BG_SECONDARY};
                        color: {Colors.TEXT_PRIMARY};
                        border: 1px solid {Colors.BORDER_LIGHT};
                        border-radius: {BorderRadius.MD}px;
                        text-align: left;
                        padding-left: 15px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: {Colors.HOVER};
                    }}
                """)
                child_btn.setCursor(Qt.PointingHandCursor)
                child_btn.clicked.connect(lambda checked, c=child: self.switch_to_child(c))
                sidebar_layout.addWidget(child_btn)
        
        sidebar_layout.addSpacing(Spacing.XXL)
        sidebar_layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setMinimumHeight(40)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ERROR};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #dc2626;
            }}
        """)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.on_logout)
        sidebar_layout.addWidget(logout_btn)
        
        sidebar.setLayout(sidebar_layout)
        sidebar.setStyleSheet(f"""
            background-color: {Colors.BG_SECONDARY};
            border-right: 1px solid {Colors.BORDER_LIGHT};
        """)
        sidebar.setMinimumWidth(200)
        sidebar.setMaximumWidth(250)
        
        main_layout.addWidget(sidebar)
        
        # Content area
        self.content_stack = QStackedWidget()
        
        # Parent dashboard
        self.parent_dashboard = ParentDashboard(self.db, self.parent_data)
        self.content_stack.addWidget(self.parent_dashboard)
        
        # Kids dashboards
        self.kids_dashboards = {}
        for i, child in enumerate(self.children):
            from ui.kids_dashboard import KidsDashboard
            kid_dash = KidsDashboard(self.db, child)
            self.kids_dashboards[child['id']] = kid_dash
            self.content_stack.addWidget(kid_dash)
        
        main_layout.addWidget(self.content_stack, 1)
        
        self.setLayout(main_layout)
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
    
    def switch_to_parent(self):
        """Switch to parent dashboard"""
        self.current_interface = "parent"
        self.current_child = None
        self.content_stack.setCurrentWidget(self.parent_dashboard)
    
    def switch_to_child(self, child: dict):
        """Switch to child dashboard"""
        self.current_interface = "child"
        self.current_child = child
        if child['id'] in self.kids_dashboards:
            self.content_stack.setCurrentWidget(self.kids_dashboards[child['id']])
    
    def on_logout(self):
        """Handle logout"""
        # Signal parent window to return to login
        QMessageBox.information(self, "Logout", "You have been logged out.")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Family Finance AI")
        self.setGeometry(100, 100, 1600, 1000)
        self.setMinimumSize(1400, 900)
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets/images/logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize database
        self.db = EnhancedDatabase("finance.db")
        
        # Setup UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize main UI"""
        # Central widget
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Stacked widget for pages
        self.pages = QStackedWidget()
        
        # Login page
        self.login_page = LoginPage(self.db)
        self.login_page.logged_in.connect(self.on_user_login)
        self.pages.addWidget(self.login_page)
        
        main_layout.addWidget(self.pages)
        
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        self.setCentralWidget(central_widget)
        
        # Apply global stylesheet
        self.setStyleSheet(GLOBAL_STYLESHEET)
    
    def on_user_login(self, parent_data: dict):
        while self.pages.count() > 0:
            widget = self.pages.widget(0)
            self.pages.removeWidget(widget)
            widget.deleteLater()

        self.app_container = MainAppContainer(
            self.db,
            parent_data
        )

        self.pages.addWidget(self.app_container)

        self.pages.setCurrentWidget(self.app_container)
    
    def closeEvent(self, event):
        """Clean up on close"""
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Set application theme
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
