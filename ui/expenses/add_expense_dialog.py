from PyQt5.QtWidgets import QDialog


class AddExpenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Expense")
        self.setFixedSize(400, 300)
