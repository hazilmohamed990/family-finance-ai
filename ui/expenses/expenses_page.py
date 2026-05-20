from datetime import datetime

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QComboBox, QDateEdit, QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget
)

from core.data_service import DataService
from ui.expenses.expense_table import ExpenseTableWidget


class ExpensesPage(QWidget):
    def __init__(self, repo, refresh_callbacks=None):
        super().__init__()
        self.repo = repo
        self.data_service = DataService(repo=self.repo)
        self.refresh_callbacks = refresh_callbacks or []
        self.selected_expense_id = None
        self._build_ui()
        self.load_expenses()

    def _build_ui(self):
        self.setStyleSheet("""
            QLabel { color: white; }
            QLineEdit, QComboBox, QDateEdit, QTextEdit {
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 14px;
                color: white;
                padding: 10px;
            }
            QPushButton {
                color: white;
                border: none;
                border-radius: 14px;
                padding: 12px 18px;
                font-weight: 700;
            }
            QPushButton#saveButton { background-color: #00C25A; }
            QPushButton#clearButton { background-color: #3B7235; }
        """)

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setSpacing(20)

        header = QLabel("Expense Manager")
        header.setStyleSheet("font-size: 26px; font-weight: 800;")
        outer_layout.addWidget(header)

        card = QFrame()
        card.setStyleSheet("""
            QFrame { background-color: rgba(255, 255, 255, 0.08); border-radius: 28px; }
        """)
        card_layout = QGridLayout()
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(18)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Rent", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description")
        self.description_input.setFixedHeight(100)

        self.add_button = QPushButton("Add Expense")
        self.add_button.setObjectName("saveButton")
        self.add_button.clicked.connect(self.on_add_expense)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.clicked.connect(self.clear_form)

        card_layout.addWidget(QLabel("Amount"), 0, 0)
        card_layout.addWidget(self.amount_input, 1, 0)
        card_layout.addWidget(QLabel("Category"), 0, 1)
        card_layout.addWidget(self.category_input, 1, 1)
        card_layout.addWidget(QLabel("Date"), 0, 2)
        card_layout.addWidget(self.date_input, 1, 2)
        card_layout.addWidget(QLabel("Description"), 2, 0, 1, 3)
        card_layout.addWidget(self.description_input, 3, 0, 1, 3)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)
        card_layout.addLayout(button_layout, 4, 0, 1, 3)

        card.setLayout(card_layout)
        outer_layout.addWidget(card)

        filter_card = QFrame()
        filter_card.setStyleSheet("""
            QFrame { background-color: rgba(255, 255, 255, 0.06); border-radius: 20px; }
        """)
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(20, 16, 20, 16)
        filter_layout.setSpacing(16)

        self.filter_category = QComboBox()
        self.filter_category.addItems(["All", "Food", "Rent", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
        self.filter_start_date = QDateEdit()
        self.filter_start_date.setCalendarPopup(True)
        self.filter_start_date.setDate(QDate.currentDate().addMonths(-3))
        self.filter_end_date = QDateEdit()
        self.filter_end_date.setCalendarPopup(True)
        self.filter_end_date.setDate(QDate.currentDate())

        self.filter_button = QPushButton("Apply Filters")
        self.filter_button.setObjectName("saveButton")
        self.filter_button.clicked.connect(self.load_expenses)

        filter_layout.addWidget(QLabel("Category"))
        filter_layout.addWidget(self.filter_category)
        filter_layout.addWidget(QLabel("From"))
        filter_layout.addWidget(self.filter_start_date)
        filter_layout.addWidget(QLabel("To"))
        filter_layout.addWidget(self.filter_end_date)
        filter_layout.addWidget(self.filter_button)
        filter_card.setLayout(filter_layout)
        outer_layout.addWidget(filter_card)

        self.expense_table = ExpenseTableWidget()
        outer_layout.addWidget(self.expense_table)

        self.setLayout(outer_layout)

    def on_add_expense(self):
        amount_text = self.amount_input.text().strip()
        description = self.description_input.toPlainText().strip()
        category = self.category_input.currentText()
        date_text = self.date_input.date().toString("yyyy-MM-dd")

        if not amount_text:
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                return
        except ValueError:
            return

        if self.selected_expense_id:
            self.data_service.update_expense(self.selected_expense_id, category, amount, date_text, description)
            self.selected_expense_id = None
            self.add_button.setText("Add Expense")
        else:
            self.data_service.add_expense(category, amount, date_text, description)

        self.clear_form()
        self.load_expenses()
        for callback in self.refresh_callbacks:
            callback()

    def clear_form(self):
        self.selected_expense_id = None
        self.add_button.setText("Add Expense")
        self.amount_input.clear()
        self.description_input.clear()
        self.category_input.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())

    def load_expenses(self):
        category_filter = self.filter_category.currentText()
        start_date = self.filter_start_date.date().toString("yyyy-MM-dd")
        end_date = self.filter_end_date.date().toString("yyyy-MM-dd")

        category = None if category_filter == "All" else category_filter
        expenses = self.data_service.get_expenses(start_date=start_date, end_date=end_date, category=category)
        self.expense_table.load_expenses(expenses, self.delete_expense, self.edit_expense)

    def delete_expense(self, expense_id):
        self.data_service.delete_expense(expense_id)
        self.load_expenses()
        for callback in self.refresh_callbacks:
            callback()

    def edit_expense(self, expense_id):
        row = next((exp for exp in self.data_service.get_expenses() if exp.id == expense_id), None)
        if not row:
            return

        self.selected_expense_id = expense_id
        self.amount_input.setText(str(row.amount))
        self.description_input.setPlainText(row.description)
        self.category_input.setCurrentText(row.category)
        try:
            self.date_input.setDate(QDate.fromString(row.date, "yyyy-MM-dd"))
        except Exception:
            self.date_input.setDate(QDate.currentDate())
        self.add_button.setText("Save Changes")
