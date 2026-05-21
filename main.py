"""
Family Finance AI - Premium Desktop Application
Modern PyQt5 UI with fintech-grade styling
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QCheckBox, QGroupBox, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy, QMessageBox, QFileDialog, QInputDialog, QSettings
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor
import sqlite3
import shutil
import tempfile
import zipfile
import csv
from datetime import datetime

# Import new modern components
from ui.theme import GLOBAL_STYLESHEET, Colors, Fonts
from ui.sidebar import ModernSidebar
from ui.dashboard import DashboardPage
from ui.transactions import ModernExpensesPage, ModernIncomePage
from ui.ai_assistant import ModernAIAssistantPage
from ui.receipt_scanner import ModernReceiptScannerPage
from ui.settings import ModernSettingsPage

# Import data services
from ai.analyzer import FinanceAnalyzer
from core.data_service import DataService
from database.queries import FinanceRepository


# Old class definitions removed - using modern components instead


class MainWindow(QMainWindow):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        try:
            from ai.chatbot import FinanceChatbot
            self.chatbot = FinanceChatbot()
        except Exception:
            self.chatbot = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        header = QLabel('AI Assistant')
        header.setStyleSheet('font-size:20px; font-weight:800;')
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText('Ask about budgeting, spending, or upload receipts for analysis')
        send_btn = QPushButton('Send')
        send_btn.clicked.connect(self.send_message)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(send_btn)
        layout.addWidget(header)
        layout.addWidget(self.chat_area)
        layout.addLayout(input_layout)
        self.setLayout(layout)
        self.load_ai_summary()

    def load_ai_summary(self):
        try:
            income, expenses = self.repo.get_financial_data(1)
            analyzer = FinanceAnalyzer(income, expenses)
            text = f"Account summary — Income: ${income:,.2f}  Expenses: ${analyzer.total_expenses():,.2f}  Savings: ${analyzer.savings():,.2f}\n"
            for insight in analyzer.insights():
                text += f"• {insight}\n"
            self.chat_area.append(text)
        except Exception:
            self.chat_area.append('Unable to load financial summary.')

    def send_message(self):
        message = self.input_line.text().strip()
        if not message:
            return
        self.chat_area.append(f"You: {message}")
        self.input_line.clear()
        if not self.chatbot:
            self.chat_area.append('AI assistant unavailable (OpenAI not configured).')
            return
        try:
            income, expenses = self.repo.get_financial_data(1)
            response = self.chatbot.respond(message, income=income, expenses=expenses)
            self.chat_area.append(f"Assistant: {response}")
        except Exception as e:
            self.chat_area.append(f"Assistant (error): {e}")


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('FamilyFinanceAI', 'FamilyFinanceAI')
        self.db_path = os.path.join(os.path.dirname(__file__), 'finance.db')
        self.init_ui()
        self.load_profile()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle('Settings')
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(18)
        font = QFont('Segoe UI', 10)
        self.setFont(font)
        self.profile_group = self.create_section('Profile')
        self.username_label = QLabel()
        self.email_label = QLabel()
        self.username_label.setStyleSheet('color: rgba(234,248,234,1); font-weight: 700;')
        self.email_label.setStyleSheet('color: rgba(234,248,234,0.9);')
        btn_username = QPushButton('Change Username')
        btn_email = QPushButton('Change Email')
        btn_username.setCursor(Qt.PointingHandCursor)
        btn_email.setCursor(Qt.PointingHandCursor)
        btn_username.clicked.connect(self.change_username)
        btn_email.clicked.connect(self.change_email)
        row = QHBoxLayout()
        col = QVBoxLayout()
        col.addWidget(self.username_label)
        col.addWidget(self.email_label)
        row.addLayout(col)
        btns = QVBoxLayout()
        btns.setSpacing(8)
        btns.addWidget(btn_username)
        btns.addWidget(btn_email)
        row.addLayout(btns)
        self.profile_group.layout().addLayout(row)
        self.main_layout.addWidget(self.profile_group)
        self.prefs_group = self.create_section('App Preferences')
        self.dark_toggle = QCheckBox('Dark Mode')
        self.anim_toggle = QCheckBox('Animations')
        self.dark_toggle.setCursor(Qt.PointingHandCursor)
        self.anim_toggle.setCursor(Qt.PointingHandCursor)
        self.dark_toggle.stateChanged.connect(self.toggle_dark_mode)
        self.anim_toggle.stateChanged.connect(self.toggle_animations)
        self.reset_theme_btn = QPushButton('Reset Theme')
        self.reset_theme_btn.setCursor(Qt.PointingHandCursor)
        self.reset_theme_btn.clicked.connect(self.reset_theme)
        pref_layout = QHBoxLayout()
        pref_left = QVBoxLayout()
        pref_left.addWidget(self.dark_toggle)
        pref_left.addWidget(self.anim_toggle)
        pref_layout.addLayout(pref_left)
        pref_right = QVBoxLayout()
        pref_right.addWidget(self.reset_theme_btn, alignment=Qt.AlignRight)
        pref_right.addStretch()
        pref_layout.addLayout(pref_right)
        self.prefs_group.layout().addLayout(pref_layout)
        self.main_layout.addWidget(self.prefs_group)
        self.data_group = self.create_section('Data Management')
        self.clear_btn = QPushButton('Clear All Data')
        self.export_btn = QPushButton('Export Data')
        self.import_btn = QPushButton('Import Data')
        for b in (self.clear_btn, self.export_btn, self.import_btn):
            b.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_all_data)
        self.export_btn.clicked.connect(self.export_data)
        self.import_btn.clicked.connect(self.import_data)
        data_layout = QHBoxLayout()
        data_left = QVBoxLayout()
        data_left.addWidget(self.clear_btn)
        data_left.addWidget(self.export_btn)
        data_left.addWidget(self.import_btn)
        data_layout.addLayout(data_left)
        self.data_group.layout().addLayout(data_layout)
        self.main_layout.addWidget(self.data_group)
        self.about_group = self.create_section('About')
        version_label = QLabel('App Version: 1.0.0')
        dev_label = QLabel('Developer: Hazil Mohamed')
        version_label.setStyleSheet('color: rgba(234,248,234,1); font-weight: 700;')
        dev_label.setStyleSheet('color: rgba(234,248,234,0.9);')
        update_btn = QPushButton('Check for Updates')
        update_btn.setCursor(Qt.PointingHandCursor)
        update_btn.clicked.connect(self.check_updates)
        about_layout = QVBoxLayout()
        about_layout.addWidget(version_label)
        about_layout.addWidget(dev_label)
        about_layout.addWidget(update_btn, alignment=Qt.AlignLeft)
        self.about_group.layout().addLayout(about_layout)
        self.main_layout.addWidget(self.about_group)
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setMinimumWidth(680)
        self.setStyleSheet(self.base_stylesheet())

    def create_section(self, title):
        box = QGroupBox(title)
        box.setLayout(QVBoxLayout())
        box.layout().setContentsMargins(14, 12, 14, 12)
        box.setStyleSheet('QGroupBox { border-radius: 14px; margin-top: 8px; padding-top: 8px; color: rgba(234,248,234,0.95); font-weight: 700; }')
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(22)
        effect.setOffset(0, 10)
        effect.setColor(QColor(0, 0, 0, 120))
        box.setGraphicsEffect(effect)
        return box

    def load_profile(self):
        username = self.settings.value('profile/username', 'Guest')
        email = self.settings.value('profile/email', 'guest@example.com')
        dark = self.settings.value('theme/dark', False)
        animations = self.settings.value('theme/animations', True)
        if isinstance(dark, str):
            dark = dark.lower() in ('true', '1', 'yes')
        if isinstance(animations, str):
            animations = animations.lower() in ('true', '1', 'yes')
        self.username_label.setText(f'Username: {username}')
        self.email_label.setText(f'Email: {email}')
        self.dark_toggle.setChecked(bool(dark))
        self.anim_toggle.setChecked(bool(animations))

    def change_username(self):
        current = self.settings.value('profile/username', '')
        text, ok = QInputDialog.getText(self, 'Change Username', 'New username:', text=current)
        if ok and text.strip():
            self.settings.setValue('profile/username', text.strip())
            self.username_label.setText(f'Username: {text.strip()}')
            QMessageBox.information(self, 'Profile', 'Username updated.')

    def change_email(self):
        current = self.settings.value('profile/email', '')
        text, ok = QInputDialog.getText(self, 'Change Email', 'New email:', text=current)
        if ok and text.strip():
            self.settings.setValue('profile/email', text.strip())
            self.email_label.setText(f'Email: {text.strip()}')
            QMessageBox.information(self, 'Profile', 'Email updated.')

    def toggle_dark_mode(self, state):
        value = bool(state)
        self.settings.setValue('theme/dark', value)
        self.apply_theme()

    def toggle_animations(self, state):
        value = bool(state)
        self.settings.setValue('theme/animations', value)
        QMessageBox.information(self, 'Animations', 'Animations setting saved.')

    def reset_theme(self):
        self.settings.setValue('theme/dark', False)
        self.settings.setValue('theme/animations', True)
        self.load_profile()
        self.apply_theme()
        QMessageBox.information(self, 'Theme', 'Theme reset to defaults.')

    def clear_all_data(self):
        reply = QMessageBox.question(self, 'Confirm Clear', 'This will delete all data in the local database. Continue?', QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        if not os.path.exists(self.db_path):
            QMessageBox.information(self, 'No Database', 'Database file not found.')
            return
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = OFF;")
            cur.execute("BEGIN TRANSACTION;")
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [r[0] for r in cur.fetchall()]
            for t in tables:
                cur.execute(f'DELETE FROM "{t}";')
                cur.execute('DELETE FROM sqlite_sequence WHERE name=?;', (t,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Cleared', 'All data cleared successfully.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to clear data: {e}')

    def export_data(self):
        options = QFileDialog.Options()
        path, _ = QFileDialog.getSaveFileName(self, 'Export Data', 'finance_export.zip', 'Zip Archive (*.zip);;Database File (*.db)', options=options)
        if not path:
            return
        try:
            if path.lower().endswith('.db'):
                if os.path.exists(self.db_path):
                    shutil.copy2(self.db_path, path)
                    QMessageBox.information(self, 'Export', 'Database copied successfully.')
                else:
                    QMessageBox.warning(self, 'Export', 'No database file found to export.')
                return
            if path.lower().endswith('.zip'):
                if not os.path.exists(self.db_path):
                    QMessageBox.warning(self, 'Export', 'No database file found to export.')
                    return
                conn = sqlite3.connect(self.db_path)
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = [r[0] for r in cur.fetchall()]
                tempdir = tempfile.mkdtemp()
                files = []
                for t in tables:
                    csv_path = os.path.join(tempdir, f'{t}.csv')
                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        cur.execute(f'SELECT * FROM "{t}" LIMIT 0;')
                        cols = [d[0] for d in cur.description] if cur.description else []
                        if cols:
                            writer.writerow(cols)
                            for row in cur.execute(f'SELECT * FROM "{t}"'):
                                writer.writerow(row)
                    files.append(csv_path)
                conn.close()
                with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for f in files:
                        zf.write(f, os.path.basename(f))
                shutil.rmtree(tempdir)
                QMessageBox.information(self, 'Export', 'Exported database tables to zip (CSV).')
                return
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, path)
                QMessageBox.information(self, 'Export', 'Export completed.')
            else:
                QMessageBox.warning(self, 'Export', 'No database file found to export.')
        except Exception as e:
            QMessageBox.critical(self, 'Export Error', f'Export failed: {e}')

    def import_data(self):
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(self, 'Import Data', '', 'Zip Archive (*.zip);;Database File (*.db);;All Files (*)', options=options)
        if not path:
            return
        reply = QMessageBox.question(self, 'Confirm Import', 'Importing will overwrite or merge data. A backup will be created. Continue?', QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        try:
            if path.lower().endswith('.db'):
                if os.path.exists(self.db_path):
                    bak = f'{self.db_path}.bak.{datetime.now().strftime("%Y%m%d%H%M%S")}'
                    shutil.copy2(self.db_path, bak)
                shutil.copy2(path, self.db_path)
                QMessageBox.information(self, 'Import', 'Database imported. Restart may be required.')
                return
            if path.lower().endswith('.zip'):
                tempdir = tempfile.mkdtemp()
                with zipfile.ZipFile(path, 'r') as zf:
                    zf.extractall(tempdir)
                conn = sqlite3.connect(self.db_path)
                cur = conn.cursor()
                for fname in os.listdir(tempdir):
                    if not fname.lower().endswith('.csv'):
                        continue
                    table = os.path.splitext(fname)[0]
                    csvfile = os.path.join(tempdir, fname)
                    with open(csvfile, newline='', encoding='utf-8') as cf:
                        reader = csv.reader(cf)
                        header = next(reader, None)
                        if not header:
                            continue
                        cols = [f'"{c}" TEXT' for c in header]
                        cur.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({", ".join(cols)});')
                        placeholders = ','.join('?' for _ in header)
                        insert_sql = f'INSERT INTO "{table}" ({", ".join([f"\"{c}\"" for c in header])}) VALUES ({placeholders});'
                        rows = [r for r in reader]
                        if rows:
                            cur.executemany(insert_sql, rows)
                conn.commit()
                conn.close()
                shutil.rmtree(tempdir)
                QMessageBox.information(self, 'Import', 'Imported CSV data from zip. Restart may be required.')
                return
            QMessageBox.warning(self, 'Import', 'Unsupported file type.')
        except Exception as e:
            QMessageBox.critical(self, 'Import Error', f'Import failed: {e}')

    def check_updates(self):
        QMessageBox.information(self, 'Updates', 'No updates available at this time.')

    def apply_theme(self):
        dark = self.settings.value('theme/dark', False)
        if isinstance(dark, str):
            dark = dark.lower() in ('true', '1', 'yes')
        if dark:
            app_style = """
                QWidget { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(12,20,12,230), stop:1 rgba(25,40,25,235)); }
            """
        else:
            app_style = "QWidget { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(245,251,245,250), stop:1 rgba(232,245,232,250)); }"
        self.setStyleSheet(self.base_stylesheet() + app_style)

    def base_stylesheet(self):
        return """
        QGroupBox { background-color: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; }
        QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #82C462, stop:0.6 #00C25A, stop:1 #3B7235); color: #062406; border-radius: 10px; padding: 8px 14px; font-weight: 700; }
        QPushButton:hover { opacity: 0.95; }
        QCheckBox { color: rgba(234,248,234,0.95); font-weight: 700; }
        QLabel { color: rgba(234,248,234,0.95); }
        """

class MainWindow(QMainWindow):
    """Modern fintech-grade main window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Family Finance AI")
        self.setGeometry(0, 0, 1920, 1080)
        self.setMinimumSize(1200, 800)
        
        # Set window icon
        icon_path = "assets/images/logo.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize data layer
        self.repo = FinanceRepository()
        self.data_service = DataService(repo=self.repo)
        
        # Initialize pages
        self._init_pages()
        
        # Setup UI
        self._setup_ui()
        
        # Apply theme
        self._apply_theme()
    
    def _init_pages(self):
        """Initialize all application pages"""
        try:
            # Dashboard
            self.dashboard = DashboardPage(self.data_service)
            
            # AI Assistant
            self.ai_assistant = ModernAIAssistantPage(self.repo)
            
            # Transactions with refresh callbacks
            refresh_callbacks = [self.dashboard.refresh, self.ai_assistant.load_ai_summary]
            self.expenses = ModernExpensesPage(self.repo, refresh_callbacks=refresh_callbacks)
            self.income = ModernIncomePage(self.repo, refresh_callback=self.ai_assistant.load_ai_summary)
            
            # Receipt scanner
            self.receipt_scanner = ModernReceiptScannerPage(self.repo, refresh_callbacks=refresh_callbacks)
            
            # Settings
            self.settings = ModernSettingsPage()
            
            # Store pages in order
            self.pages = [
                self.dashboard,
                self.expenses,
                self.income,
                self.ai_assistant,
                self.receipt_scanner,
                self.settings,
            ]
        except Exception as e:
            print(f"Error initializing pages: {e}")
            import traceback
            traceback.print_exc()
    
    def _setup_ui(self):
        """Setup main UI layout"""
        try:
            # Central widget
            central_widget = QWidget()
            main_layout = QHBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)
            
            # Sidebar
            self.sidebar = ModernSidebar()
            self.sidebar.setFixedWidth(200)
            self.sidebar.page_switched.connect(self._switch_page)
            
            # Stack widget for pages
            self.stack = QStackedWidget()
            for page in self.pages:
                self.stack.addWidget(page)
            
            # Add to layout
            main_layout.addWidget(self.sidebar)
            main_layout.addWidget(self.stack, 1)
            
            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)
        except Exception as e:
            print(f"Error setting up UI: {e}")
            import traceback
            traceback.print_exc()
    
    def _switch_page(self, page_index: int):
        """Switch to page"""
        self.stack.setCurrentIndex(page_index)
    
    def _apply_theme(self):
        """Apply global theme stylesheet"""
        self.setStyleSheet(GLOBAL_STYLESHEET)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(Fonts.body_base())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())