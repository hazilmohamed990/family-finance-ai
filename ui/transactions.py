"""
Modern Expenses and Income Pages
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox,
    QDoubleSpinBox, QDateEdit, QDialog, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from .theme import Colors, Fonts, Spacing, BorderRadius
from .components import (
    Card, PrimaryButton, SecondaryButton, DangerButton, SuccessButton, VSection,
    StyledLineEdit, StyledComboBox, AmountInput, Separator
)


class TransactionRow(QFrame):
    """A single transaction row card"""
    
    delete_requested = pyqtSignal(int)
    
    def __init__(self, transaction_id: int, date: str, description: str, category: str, amount: float, parent=None):
        super().__init__(parent)
        self.transaction_id = transaction_id
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.MD}px;
            }}
            QFrame:hover {{
                background-color: {Colors.HOVER};
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(Spacing.MD, Spacing.SM, Spacing.MD, Spacing.SM)
        layout.setSpacing(Spacing.MD)
        
        # Date
        date_label = QLabel(date)
        date_label.setFont(Fonts.body_sm())
        date_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        date_label.setFixedWidth(80)
        layout.addWidget(date_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setFont(Fonts.body_base())
        desc_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(desc_label, 1)
        
        # Category
        cat_label = QLabel(category)
        cat_label.setFont(Fonts.label_small())
        cat_label.setStyleSheet(f"""
            background-color: {Colors.BG_TERTIARY};
            color: {Colors.TEXT_SECONDARY};
            padding: 4px 8px;
            border-radius: {BorderRadius.SM}px;
        """)
        cat_label.setFixedWidth(100)
        layout.addWidget(cat_label)
        
        # Amount
        amount_label = QLabel(f"${amount:,.2f}")
        amount_label.setFont(Fonts.heading_5())
        amount_label.setStyleSheet(f"color: {Colors.EXPENSE};")
        amount_label.setFixedWidth(100)
        layout.addWidget(amount_label)
        
        # Delete button
        delete_btn = DangerButton("Delete")
        delete_btn.setFixedWidth(80)
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.transaction_id))
        layout.addWidget(delete_btn)
        
        self.setLayout(layout)
        self.setFixedHeight(60)


class ModernExpensesPage(QWidget):
    """Modern expenses tracking page"""
    
    def __init__(self, repo, refresh_callbacks=None, parent=None):
        super().__init__(parent)
        self.repo = repo
        self.refresh_callbacks = refresh_callbacks or []
        self.init_ui()
        self.load_expenses()
    
    def init_ui(self):
        """Initialize expenses UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(Spacing.SM)
        
        title = QLabel("Expense Tracker")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        subtitle = QLabel("Track and manage your spending")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Add expense form
        form_section = VSection("Add New Expense")
        form_layout = QGridLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(Spacing.MD)
        
        # Description
        self.desc_input = StyledLineEdit("Description")
        form_layout.addWidget(QLabel("Description"), 0, 0)
        form_layout.addWidget(self.desc_input, 1, 0)
        
        # Amount
        self.amount_input = AmountInput()
        form_layout.addWidget(QLabel("Amount"), 0, 1)
        form_layout.addWidget(self.amount_input, 1, 1)
        
        # Category
        self.category_combo = StyledComboBox()
        self.category_combo.addItems([
            "Food", "Transport", "Entertainment", "Utilities",
            "Healthcare", "Shopping", "Other"
        ])
        form_layout.addWidget(QLabel("Category"), 0, 2)
        form_layout.addWidget(self.category_combo, 1, 2)
        
        # Date
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet(f"""
            QDateEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 8px 12px;
                font-size: 13px;
            }}
            QDateEdit:focus {{
                border: 1px solid {Colors.ACCENT};
            }}
        """)
        self.date_input.setMinimumHeight(40)
        form_layout.addWidget(QLabel("Date"), 0, 3)
        form_layout.addWidget(self.date_input, 1, 3)
        
        # Add button
        add_btn = PrimaryButton("Add Expense")
        add_btn.clicked.connect(self.add_expense)
        form_layout.addWidget(add_btn, 1, 4)
        
        form_section.content_layout.addLayout(form_layout)
        main_layout.addWidget(form_section)
        
        main_layout.addWidget(Separator())
        
        # Expenses list
        list_section = VSection("Recent Expenses")
        self.expenses_layout = QVBoxLayout()
        self.expenses_layout.setContentsMargins(0, 0, 0, 0)
        self.expenses_layout.setSpacing(Spacing.MD)
        self.expenses_layout.addStretch()
        list_section.content_layout.addLayout(self.expenses_layout)
        
        main_layout.addWidget(list_section, 1)
        
        self.setLayout(main_layout)
    
    def load_expenses(self):
        """Load and display expenses"""
        try:
            # Clear layout
            while self.expenses_layout.count() > 1:
                self.expenses_layout.takeAt(0).widget().deleteLater()
            
            expenses = self.repo.get_expenses(1)
            for exp in expenses:
                row = TransactionRow(
                    exp[0],
                    exp[3] if len(exp) > 3 else '',
                    exp[4] if len(exp) > 4 else '',
                    exp[1] if len(exp) > 1 else '',
                    exp[2] if len(exp) > 2 else 0,
                )
                row.delete_requested.connect(self.delete_expense)
                self.expenses_layout.insertWidget(self.expenses_layout.count() - 1, row)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load expenses: {e}")
    
    def add_expense(self):
        """Add new expense"""
        try:
            description = self.desc_input.text().strip()
            amount = self.amount_input.value()
            category = self.category_combo.currentText()
            date = self.date_input.date().toString("yyyy-MM-dd")
            
            if not description or amount <= 0:
                QMessageBox.warning(self, "Validation", "Please fill in all fields correctly")
                return
            
            self.repo.add_expense(1, category, amount, date, description)
            self.desc_input.clear()
            self.amount_input.setValue(0)
            self.date_input.setDate(QDate.currentDate())
            
            self.load_expenses()
            for callback in self.refresh_callbacks:
                callback()
            
            QMessageBox.information(self, "Success", "Expense added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add expense: {e}")
    
    def delete_expense(self, expense_id: int):
        """Delete expense"""
        try:
            reply = QMessageBox.question(self, "Confirm", "Delete this expense?")
            if reply == QMessageBox.Yes:
                self.repo.delete_expense(expense_id)
                self.load_expenses()
                for callback in self.refresh_callbacks:
                    callback()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete expense: {e}")


class ModernIncomePage(QWidget):
    """Modern income tracking page"""
    
    def __init__(self, repo, refresh_callback=None, parent=None):
        super().__init__(parent)
        self.repo = repo
        self.refresh_callback = refresh_callback
        self.init_ui()
        self.load_income()
    
    def init_ui(self):
        """Initialize income UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(Spacing.SM)
        
        title = QLabel("Income Tracker")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        subtitle = QLabel("Track and manage your income sources")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Add income form
        form_section = VSection("Add New Income")
        form_layout = QGridLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(Spacing.MD)
        
        # Source
        self.source_input = StyledLineEdit("Income Source")
        form_layout.addWidget(QLabel("Source"), 0, 0)
        form_layout.addWidget(self.source_input, 1, 0)
        
        # Amount
        self.amount_input = AmountInput()
        form_layout.addWidget(QLabel("Amount"), 0, 1)
        form_layout.addWidget(self.amount_input, 1, 1)
        
        # Date
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet(f"""
            QDateEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 8px 12px;
                font-size: 13px;
            }}
            QDateEdit:focus {{
                border: 1px solid {Colors.ACCENT};
            }}
        """)
        self.date_input.setMinimumHeight(40)
        form_layout.addWidget(QLabel("Date"), 0, 2)
        form_layout.addWidget(self.date_input, 1, 2)
        
        # Add button
        add_btn = SuccessButton("Add Income")
        add_btn.clicked.connect(self.add_income)
        form_layout.addWidget(add_btn, 1, 3)
        
        form_section.content_layout.addLayout(form_layout)
        main_layout.addWidget(form_section)
        
        main_layout.addWidget(Separator())
        
        # Income list
        list_section = VSection("Recent Income")
        self.income_layout = QVBoxLayout()
        self.income_layout.setContentsMargins(0, 0, 0, 0)
        self.income_layout.setSpacing(Spacing.MD)
        self.income_layout.addStretch()
        list_section.content_layout.addLayout(self.income_layout)
        
        main_layout.addWidget(list_section, 1)
        
        self.setLayout(main_layout)
    
    def load_income(self):
        """Load and display income"""
        try:
            # Clear layout
            while self.income_layout.count() > 1:
                self.income_layout.takeAt(0).widget().deleteLater()
            
            income_items = self.repo.get_income(1)
            for inc in income_items:
                row = TransactionRow(
                    inc[0],
                    inc[3] if len(inc) > 3 else '',
                    inc[2] if len(inc) > 2 else '',
                    "Income",
                    inc[1] if len(inc) > 1 else 0,
                )
                row.delete_requested.connect(self.delete_income)
                self.income_layout.insertWidget(self.income_layout.count() - 1, row)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load income: {e}")
    
    def add_income(self):
        """Add new income"""
        try:
            source = self.source_input.text().strip()
            amount = self.amount_input.value()
            date = self.date_input.date().toString("yyyy-MM-dd")
            
            if not source or amount <= 0:
                QMessageBox.warning(self, "Validation", "Please fill in all fields correctly")
                return
            
            self.repo.add_income(1, amount, source, date)
            self.source_input.clear()
            self.amount_input.setValue(0)
            self.date_input.setDate(QDate.currentDate())
            
            self.load_income()
            if self.refresh_callback:
                self.refresh_callback()
            
            QMessageBox.information(self, "Success", "Income added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add income: {e}")
    
    def delete_income(self, income_id: int):
        """Delete income"""
        try:
            reply = QMessageBox.question(self, "Confirm", "Delete this income?")
            if reply == QMessageBox.Yes:
                self.repo.delete_income(income_id)
                self.load_income()
                if self.refresh_callback:
                    self.refresh_callback()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete income: {e}")

