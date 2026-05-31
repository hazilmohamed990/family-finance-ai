from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from utils.app_helpers import PasswordHelper, FileHelper
from database.enhanced_db import EnhancedDatabase


class LoginPage(QWidget):
    """Simple login widget used at app startup. Emits `logged_in(parent_id)` on success."""
    logged_in = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = EnhancedDatabase()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Welcome — Sign in")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px;font-weight:700;")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        btn_layout = QHBoxLayout()
        login_btn = QPushButton("Sign In")
        signup_btn = QPushButton("Create Account")

        login_btn.clicked.connect(self._do_login)
        signup_btn.clicked.connect(self._open_signup)

        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(signup_btn)

        layout.addWidget(title)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _do_login(self):
        email = self.email.text().strip()
        pwd = self.password.text()
        if not email or not pwd:
            QMessageBox.warning(self, "Missing", "Please enter email and password.")
            return
        parent = self.db.get_parent_by_email(email)
        if not parent:
            QMessageBox.warning(self, "Not found", "No account found for that email.")
            return
        if PasswordHelper.verify_password(pwd, parent['password_hash']):
            QMessageBox.information(self, "Welcome", f"Signed in as {parent['name']}")
            self.logged_in.emit(parent['id'])
        else:
            QMessageBox.critical(self, "Invalid", "Incorrect password.")

    def _open_signup(self):
        from .signup_page import SignupPage
        dlg = SignupPage(parent=self)
        dlg.account_created.connect(lambda pid: self.logged_in.emit(pid))
        dlg.exec_()
