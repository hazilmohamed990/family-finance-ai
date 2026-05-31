from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from database.enhanced_db import EnhancedDatabase
from utils.app_helpers import PasswordHelper


class SignupPage(QDialog):
    """Simple signup dialog to create a parent account."""
    account_created = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = EnhancedDatabase()
        self.setWindowTitle("Create Account")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Full name")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.password2 = QLineEdit()
        self.password2.setPlaceholderText("Confirm password")
        self.password2.setEchoMode(QLineEdit.Password)

        create_btn = QPushButton("Create Account")
        create_btn.clicked.connect(self._create_account)

        layout.addWidget(QLabel("Create an account"))
        layout.addWidget(self.name)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.password2)
        layout.addWidget(create_btn)

        self.setLayout(layout)

    def _create_account(self):
        name = self.name.text().strip()
        email = self.email.text().strip()
        p1 = self.password.text()
        p2 = self.password2.text()

        if not name or not email or not p1:
            QMessageBox.warning(self, "Missing", "Please complete all fields.")
            return
        if p1 != p2:
            QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return
        existing = self.db.get_parent_by_email(email)
        if existing:
            QMessageBox.warning(self, "Exists", "An account with that email already exists.")
            return
        pwd_hash = PasswordHelper.hash_password(p1)
        try:
            pid = self.db.add_parent(email, name, pwd_hash)
            QMessageBox.information(self, "Created", "Account created successfully.")
            self.account_created.emit(pid)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create account: {e}")
