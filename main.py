import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

from ai.analyzer import FinanceAnalyzer
from core.data_service import DataService
from database.queries import FinanceRepository
from ui.dashboard.dashboard_page import DashboardPage
from ui.expenses.expenses_page import ExpensesPage


class Sidebar(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        title = QLabel()
        title.setAlignment(Qt.AlignCenter)
        title.setPixmap(QPixmap("assets/images/logo.png").scaled(
            160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

        def create_button(icon_path, index):
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(28, 28))
            btn.setFixedSize(72, 72)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda: self.switch_page_callback(index))
            btn.setStyleSheet("background-color: rgba(255, 255, 255, 0.08); border-radius: 18px;")
            return btn

        btn_dashboard = create_button("assets/icons/dashboard.png", 0)
        btn_expenses = create_button("assets/icons/expenses.png", 1)
        btn_income = create_button("assets/icons/income.png", 2)
        btn_ai = create_button("assets/icons/ai.png", 3)
        btn_settings = create_button("assets/icons/settings.png", 4)

        layout.addWidget(title)
        layout.addSpacing(12)
        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_expenses)
        layout.addWidget(btn_income)
        layout.addWidget(btn_ai)
        layout.addWidget(btn_settings)
        layout.addStretch()

        self.setLayout(layout)


class IncomePage(QWidget):
    def __init__(self, repo, refresh_ai_callback):
        super().__init__()
        self.repo = repo
        self.refresh_ai_callback = refresh_ai_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        title = QLabel("Add Income")
        title.setStyleSheet("font-size: 28px; font-weight: 800;")

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Income Amount")
        self.source = QLineEdit()
        self.source.setPlaceholderText("Income Source")

        add_btn = QPushButton("Add Income")
        add_btn.clicked.connect(self.add_income)
        add_btn.setStyleSheet("background-color: #00C25A; color: white; border-radius: 14px; padding: 12px;")

        layout.addWidget(title)
        layout.addWidget(self.amount)
        layout.addWidget(self.source)
        layout.addWidget(add_btn)
        layout.addStretch()
        self.setLayout(layout)

    def add_income(self):
        try:
            amount = float(self.amount.text())
            source = self.source.text().strip()
            if amount <= 0 or not source:
                return
            date = datetime.now().strftime("%Y-%m-%d")
            self.repo.add_income(1, amount, source, date)
            self.amount.clear()
            self.source.clear()
            self.refresh_ai_callback()
        except ValueError:
            return


class AIAssistantPage(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 16px; line-height: 1.5;")

        layout.addWidget(self.label)
        self.setLayout(layout)
        self.load_ai()

    def load_ai(self):
        income, expenses = self.repo.get_financial_data(1)
        analyzer = FinanceAnalyzer(income, expenses)

        text = f"Income: ${income:,.2f}\n"
        text += f"Expenses: ${analyzer.total_expenses():,.2f}\n"
        text += f"Savings: ${analyzer.savings():,.2f}\n\n"

        for insight in analyzer.insights():
            text += f"• {insight}\n"

        self.label.setText(text)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        label = QLabel("Settings")
        label.setStyleSheet("font-size: 28px; font-weight: 800;")
        layout.addWidget(label)
        layout.addStretch()
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Family Finance AI")
        self.setGeometry(0, 0, 1920, 1080)

        self.repo = FinanceRepository()
        self.data_service = DataService(repo=self.repo)

        self.dashboard = DashboardPage(self.data_service)
        self.ai = AIAssistantPage(self.repo)
        self.expenses = ExpensesPage(
            self.repo,
            refresh_callbacks=[self.dashboard.refresh, self.ai.load_ai]
        )
        self.income = IncomePage(self.repo, self.ai.load_ai)
        self.settings = SettingsPage()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.expenses)
        self.stack.addWidget(self.income)
        self.stack.addWidget(self.ai)
        self.stack.addWidget(self.settings)

        self.sidebar = Sidebar(self.switch_page)
        self.sidebar.setFixedWidth(220)

        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        self.apply_style()

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #08121B;
            }
            QWidget {
                color: #E4F1D1;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #E4F1D1;
            }
            QPushButton {
                background-color: #1C2A36;
                color: #E4F1D1;
                border: 1px solid rgba(180, 222, 139, 0.22);
                border-radius: 16px;
                padding: 12px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: rgba(0, 194, 90, 0.18);
            }
            QLineEdit, QComboBox, QDateEdit, QTextEdit {
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 14px;
                color: #E4F1D1;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
