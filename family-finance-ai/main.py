import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QPushButton, QLabel, QStackedWidget, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QPixmap, QIcon

from ai.analyzer import FinanceAnalyzer
from database.queries import FinanceRepository


class Sidebar(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel()
        title.setAlignment(Qt.AlignCenter)
        title.setPixmap(QPixmap("assets/images/logo.png").scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

        def icon_btn(path, index):
            btn = QPushButton()
            btn.setIcon(QIcon(path))
            btn.setIconSize(Qt.QSize(28, 28))
            btn.clicked.connect(lambda: self.switch_page_callback(index))
            return btn

        btn_dashboard = QPushButton()
        btn_dashboard.setIcon(QIcon("assets/icons/dashboard.png"))
        btn_dashboard.clicked.connect(lambda: self.switch_page_callback(0))

        btn_expenses = QPushButton()
        btn_expenses.setIcon(QIcon("assets/icons/expenses.png"))
        btn_expenses.clicked.connect(lambda: self.switch_page_callback(1))

        btn_income = QPushButton()
        btn_income.setIcon(QIcon("assets/icons/income.png"))
        btn_income.clicked.connect(lambda: self.switch_page_callback(2))

        btn_ai = QPushButton()
        btn_ai.setIcon(QIcon("assets/icons/ai.png"))
        btn_ai.clicked.connect(lambda: self.switch_page_callback(3))

        btn_settings = QPushButton()
        btn_settings.setIcon(QIcon("assets/icons/settings.png"))
        btn_settings.clicked.connect(lambda: self.switch_page_callback(4))

        for b in [btn_dashboard, btn_expenses, btn_income, btn_ai, btn_settings]:
            b.setFixedSize(60, 60)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_expenses)
        layout.addWidget(btn_income)
        layout.addWidget(btn_ai)
        layout.addWidget(btn_settings)
        layout.addStretch()

        self.setLayout(layout)


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(20, 220, 20, 20)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        top_grid = QGridLayout()
        top_grid.setSpacing(12)


        top_card_colors = ["#3B7235", "#82C462", "#B4DE8B", "#00C25A"]

        top_card_labels = [
            "Account Balance\n$0.00",
            "Total Income\n$0.00",
            "Total Expenses\n$0.00",
            "Net Savings\n$0.00"
        ]

        for i in range(4):
            card = QFrame()
            card.setFixedSize(270, 140)

            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {top_card_colors[i]};
                    border-radius: 16px;
                }}
            """)

            layout = QVBoxLayout()
            label = QLabel(top_card_labels[i])
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

            layout.addStretch()
            layout.addWidget(label)
            layout.addStretch()

            card.setLayout(layout)
            top_grid.addWidget(card, 0, i)

        main_layout.addLayout(top_grid)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)
        bottom_layout.setAlignment(Qt.AlignLeft)

        left_side = QVBoxLayout()
        left_side.setSpacing(12)

        bottom_rect_colors = ["#3B7235", "#82C462"]
        bottom_rect_labels = ["Recent Transactions", "Budget Breakdown"]

        for i in range(2):
            rect = QFrame()
            rect.setFixedSize(830, 140)

            rect.setStyleSheet(f"""
                QFrame {{
                    background-color: {bottom_rect_colors[i]};
                    border-radius: 18px;
                }}
            """)

            layout = QVBoxLayout()

            label = QLabel(bottom_rect_labels[i])
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

            layout.addStretch()
            layout.addWidget(label)
            layout.addStretch()

            rect.setLayout(layout)
            left_side.addWidget(rect)

        side_rect = QFrame()
        side_rect.setFixedSize(260, 285)

        side_rect.setStyleSheet("""
            QFrame {
                background-color: #00C25A;
                border-radius: 20px;
            }
        """)

        side_layout = QVBoxLayout()

        side_label = QLabel("Financial Insights")
        side_label.setAlignment(Qt.AlignCenter)
        side_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

        side_layout.addStretch()
        side_layout.addWidget(side_label)
        side_layout.addStretch()

        side_rect.setLayout(side_layout)

        bottom_layout.addLayout(left_side)
        bottom_layout.addWidget(side_rect)

        main_layout.addLayout(bottom_layout)
        outer_layout.addLayout(main_layout)

        self.setLayout(outer_layout)


from PyQt5.QtWidgets import QComboBox, QLineEdit
from datetime import datetime


class ExpensesPage(QWidget):
    def __init__(self, repo, refresh_ai_callback):
        super().__init__()

        self.repo = repo
        self.refresh_ai_callback = refresh_ai_callback

        layout = QVBoxLayout()

        title = QLabel("Add Expense")
        title.setAlignment(Qt.AlignCenter)

        self.category = QComboBox()
        self.category.addItems([
            "Food",
            "Rent",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ])

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Amount")

        add_btn = QPushButton("Add Expense")
        add_btn.clicked.connect(self.add_expense)

        layout.addWidget(title)
        layout.addWidget(self.category)
        layout.addWidget(self.amount)
        layout.addWidget(add_btn)

        self.setLayout(layout)

    def add_expense(self):
        try:
            amount = float(self.amount.text())
            category = self.category.currentText()
            date = datetime.now().strftime("%Y-%m-%d")

            self.repo.add_expense(1, category, amount, date)

            self.amount.clear()

            self.refresh_ai_callback()

        except:
            pass


class IncomePage(QWidget):
    def __init__(self, repo, refresh_ai_callback):
        super().__init__()

        self.repo = repo
        self.refresh_ai_callback = refresh_ai_callback

        layout = QVBoxLayout()

        title = QLabel("Add Income")
        title.setAlignment(Qt.AlignCenter)

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Income Amount")

        self.source = QLineEdit()
        self.source.setPlaceholderText("Income Source")

        add_btn = QPushButton("Add Income")
        add_btn.clicked.connect(self.add_income)

        layout.addWidget(title)
        layout.addWidget(self.amount)
        layout.addWidget(self.source)
        layout.addWidget(add_btn)

        self.setLayout(layout)

    def add_income(self):
        try:
            amount = float(self.amount.text())
            source = self.source.text()
            date = datetime.now().strftime("%Y-%m-%d")

            self.repo.add_income(1, amount, source, date)

            self.amount.clear()
            self.source.clear()

            self.refresh_ai_callback()

        except:
            pass


class AIAssistantPage(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo

        layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignTop)
        self.label.setWordWrap(True)

        layout.addWidget(self.label)
        self.setLayout(layout)

        self.load_ai()

    def load_ai(self):
        income, expenses = self.repo.get_financial_data(1)

        analyzer = FinanceAnalyzer(income, expenses)

        text = f"Income: {income}\n"
        text += f"Expenses: {analyzer.total_expenses()}\n"
        text += f"Savings: {analyzer.savings()}\n\n"

        for i in analyzer.insights():
            text += i + "\n"

        self.label.setText(text)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Settings")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Family Finance AI")
        self.setGeometry(0, 0, 1920, 1080)

        self.repo = FinanceRepository()

        self.stack = QStackedWidget()

        self.dashboard = DashboardPage()

        self.ai = AIAssistantPage(self.repo)

        self.expenses = ExpensesPage(
            self.repo,
            self.ai.load_ai
        )

        self.income = IncomePage(
            self.repo,
            self.ai.load_ai
        )
        self.settings = SettingsPage()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.expenses)
        self.stack.addWidget(self.income)
        self.stack.addWidget(self.ai)
        self.stack.addWidget(self.settings)

        self.sidebar = Sidebar(self.switch_page)
        self.sidebar.setFixedWidth(200)

        main_widget = QWidget()
        main_layout = QHBoxLayout()

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
        background-image: url(assets/images/background.png);
        background-repeat: no-repeat;
        background-position: center;
    }

    QLabel {
        color: white;
        font-size: 18px;
        font-weight: 800;
    }

    QPushButton {
        background-color: white;
        color: white;
        padding: 10px;
        border-radius: 8px;
        border: none;
        font-size: 15px;
        font-weight: 700;
    }

    QPushButton:hover {
        background-color: #f4f4f4;
    }

    QLineEdit {
        background-color: rgba(30, 41, 59, 180);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-size: 14px;
    }

    QComboBox {
        background-color: rgba(30, 41, 59, 180);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-size: 14px;
    }
""")


def main():
    app = QApplication(sys.argv)

    font_id = QFontDatabase.addApplicationFont("assets/fonts/SF-Pro.ttf")

    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app_font = QApplication.font()
        app_font.setFamily(font_family)
        QApplication.setFont(app_font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()