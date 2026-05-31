from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database.enhanced_db import EnhancedDatabase


class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = EnhancedDatabase()
        self.setWindowTitle("Forgot Password")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        send_btn = QPushButton("Lookup Account")
        send_btn.clicked.connect(self._lookup)
        layout.addWidget(QLabel("Enter your account email"))
        layout.addWidget(self.email)
        layout.addWidget(send_btn)
        self.setLayout(layout)

    def _lookup(self):
        email = self.email.text().strip()
        if not email:
            QMessageBox.warning(self, "Missing", "Please enter your email.")
            return
        parent = self.db.get_parent_by_email(email)
        if not parent:
            QMessageBox.information(self, "Not found", "No account found for that email.")
            return
        QMessageBox.information(self, "Reminder", "We cannot reset passwords automatically in this demo. Please recreate your account if needed.")
        self.accept()
