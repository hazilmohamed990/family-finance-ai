from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QHeaderView, QPushButton, QTableWidget, QTableWidgetItem, QWidget


class ExpenseTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description", "Actions"])
        self.setColumnHidden(0, True)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.06);
                color: #E4F1D1;
                border: none;
            }
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.12);
                color: #B4DE8B;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

    def load_expenses(self, expenses, delete_callback, edit_callback):
        self.setRowCount(0)
        for expense in expenses:
            row_index = self.rowCount()
            self.insertRow(row_index)
            self.setItem(row_index, 0, QTableWidgetItem(str(expense.id)))
            self.setItem(row_index, 1, QTableWidgetItem(expense.date))
            self.setItem(row_index, 2, QTableWidgetItem(expense.category))
            self.setItem(row_index, 3, QTableWidgetItem(f"${expense.amount:,.2f}"))
            self.setItem(row_index, 4, QTableWidgetItem(expense.description))

            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(6)

            edit_button = QPushButton("Edit")
            edit_button.setProperty("expense_id", expense.id)
            edit_button.clicked.connect(lambda checked, exp_id=expense.id: edit_callback(exp_id))
            edit_button.setStyleSheet("background-color: #82C462; color: #101820; border-radius: 10px; padding: 6px 12px;")

            delete_button = QPushButton("Delete")
            delete_button.setProperty("expense_id", expense.id)
            delete_button.clicked.connect(lambda checked, exp_id=expense.id: delete_callback(exp_id))
            delete_button.setStyleSheet("background-color: #F76262; color: white; border-radius: 10px; padding: 6px 12px;")

            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_widget.setLayout(actions_layout)
            self.setCellWidget(row_index, 5, actions_widget)

        self.resizeRowsToContents()
        self.resizeColumnsToContents()
