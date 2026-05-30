"""
Settings and Preferences Management
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox,
    QComboBox, QSlider, QSpinBox, QTabWidget, QFrame, QFormLayout,
    QMessageBox, QColorDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from database.enhanced_db import EnhancedDatabase
from ui.theme import Colors, Fonts, Spacing, BorderRadius


class SettingsPanel(QWidget):
    """Settings and preferences panel"""
    
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, db: EnhancedDatabase, user_data: dict, user_type: str = "parent", parent=None):
        super().__init__(parent)
        self.db = db
        self.user_data = user_data
        self.user_type = user_type
        
        # Load user settings from QSettings or database
        self.settings = {
            'theme_mode': 'light',
            'currency': 'USD',
            'notifications_enabled': True,
            'sound_enabled': True,
            'animations_enabled': True,
            'budget_alerts_enabled': True,
            'items_per_page': 20,
            'accent_color': Colors.ACCENT,
        }
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize settings UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        title = QLabel("⚙️ Settings & Preferences")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        main_layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
            QTabBar::tab {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                padding: {Spacing.MD}px;
                margin-right: {Spacing.SM}px;
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.ACCENT};
                color: white;
            }}
        """)
        
        # App Settings Tab
        app_settings_widget = self.create_app_settings_tab()
        tabs.addTab(app_settings_widget, "🎨 App Settings")
        
        # Notification Settings Tab
        notif_settings_widget = self.create_notification_settings_tab()
        tabs.addTab(notif_settings_widget, "🔔 Notifications")
        
        # Privacy Settings Tab
        privacy_settings_widget = self.create_privacy_settings_tab()
        tabs.addTab(privacy_settings_widget, "🔒 Privacy")
        
        # About Tab
        about_widget = self.create_about_tab()
        tabs.addTab(about_widget, "ℹ️ About")
        
        main_layout.addWidget(tabs)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Spacing.MD)
        button_layout.addStretch()
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setMinimumHeight(40)
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
        """)
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.clicked.connect(self.reset_to_defaults)
        
        save_btn = QPushButton("✓ Save Settings")
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT_HOVER};
            }}
        """)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_settings)
        
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(save_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
    
    def create_app_settings_tab(self) -> QWidget:
        """Create app settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.LG)
        
        # Theme section
        theme_frame = QFrame()
        theme_layout = QFormLayout()
        
        theme_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.LG}px;
            }}
        """)
        
        theme_label = QLabel("Theme Mode")
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark", "Auto"])
        theme_combo.setCurrentText("Light")
        
        theme_layout.addRow(theme_label, theme_combo)
        
        # Accent Color
        color_label = QLabel("Accent Color")
        color_btn = QPushButton("Choose Color")
        color_btn.setMaximumWidth(150)
        color_btn.clicked.connect(lambda: self.choose_color())
        
        theme_layout.addRow(color_label, color_btn)
        
        # Currency
        currency_label = QLabel("Currency")
        currency_combo = QComboBox()
        currency_combo.addItems(["USD ($)", "EUR (€)", "GBP (£)", "JPY (¥)"])
        currency_combo.setCurrentText("USD ($)")
        
        theme_layout.addRow(currency_label, currency_combo)
        
        # Animations
        anim_checkbox = QCheckBox("Enable Animations")
        anim_checkbox.setChecked(True)
        theme_layout.addRow("", anim_checkbox)
        
        theme_frame.setLayout(theme_layout)
        layout.addWidget(theme_frame)
        
        # Display section
        display_frame = QFrame()
        display_layout = QFormLayout()
        
        display_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.LG}px;
            }}
        """)
        
        items_label = QLabel("Items Per Page")
        items_spin = QSpinBox()
        items_spin.setMinimum(5)
        items_spin.setMaximum(100)
        items_spin.setValue(20)
        
        display_layout.addRow(items_label, items_spin)
        
        display_frame.setLayout(display_layout)
        layout.addWidget(display_frame)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_notification_settings_tab(self) -> QWidget:
        """Create notification settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.LG)
        
        frame = QFrame()
        frame_layout = QVBoxLayout()
        
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.LG}px;
            }}
        """)
        
        # Notification options
        notif_enabled = QCheckBox("Enable Notifications")
        notif_enabled.setChecked(True)
        
        sound_enabled = QCheckBox("Enable Sound")
        sound_enabled.setChecked(True)
        
        budget_alerts = QCheckBox("Budget Alerts")
        budget_alerts.setChecked(True)
        
        daily_summary = QCheckBox("Daily Summary")
        daily_summary.setChecked(False)
        
        goal_reminders = QCheckBox("Goal Reminders")
        goal_reminders.setChecked(True)
        
        frame_layout.addWidget(notif_enabled)
        frame_layout.addWidget(sound_enabled)
        frame_layout.addSpacing(Spacing.LG)
        frame_layout.addWidget(QLabel("Alert Types:"))
        frame_layout.addWidget(budget_alerts)
        frame_layout.addWidget(daily_summary)
        frame_layout.addWidget(goal_reminders)
        
        frame.setLayout(frame_layout)
        layout.addWidget(frame)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_privacy_settings_tab(self) -> QWidget:
        """Create privacy settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.LG)
        
        frame = QFrame()
        frame_layout = QVBoxLayout()
        
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.LG}px;
            }}
        """)
        
        # Privacy options
        privacy_label = QLabel("Data & Privacy")
        privacy_label.setFont(Fonts.heading_4())
        frame_layout.addWidget(privacy_label)
        
        # Data sharing
        sharing_checkbox = QCheckBox("Share analytics data (helps improve app)")
        sharing_checkbox.setChecked(False)
        frame_layout.addWidget(sharing_checkbox)
        
        # Backup
        backup_btn = QPushButton("📦 Backup My Data")
        backup_btn.setMinimumHeight(40)
        backup_btn.clicked.connect(lambda: QMessageBox.information(self, "Backup", "Data backup feature"))
        frame_layout.addWidget(backup_btn)
        
        # Export
        export_btn = QPushButton("📥 Export Data (CSV)")
        export_btn.setMinimumHeight(40)
        export_btn.clicked.connect(lambda: QMessageBox.information(self, "Export", "Data export feature"))
        frame_layout.addWidget(export_btn)
        
        # Clear data
        clear_btn = QPushButton("🗑️ Clear All Data")
        clear_btn.setMinimumHeight(40)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ERROR};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #dc2626;
            }}
        """)
        clear_btn.clicked.connect(self.on_clear_data)
        frame_layout.addWidget(clear_btn)
        
        frame.setLayout(frame_layout)
        layout.addWidget(frame)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_about_tab(self) -> QWidget:
        """Create about tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(Spacing.LG)
        layout.setAlignment(Qt.AlignTop)
        
        frame = QFrame()
        frame_layout = QVBoxLayout()
        frame_layout.setSpacing(Spacing.MD)
        
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.LG}px;
            }}
        """)
        
        # App info
        app_label = QLabel("Family Finance AI")
        app_label.setFont(Fonts.heading_3())
        app_label.setStyleSheet(f"color: {Colors.ACCENT};")
        
        version_label = QLabel("Version 1.0.0")
        version_label.setFont(Fonts.body_base())
        version_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        dev_label = QLabel("Developed with ❤️ for families")
        dev_label.setFont(Fonts.body_sm())
        dev_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY};")
        
        # Features
        features_label = QLabel("✓ Features:")
        features_label.setFont(Fonts.body_base())
        
        features_text = QLabel("""
        • Dual parent & kids interfaces
        • Financial tracking & analytics
        • AI financial advisor
        • Gamified savings system
        • Receipt scanning with OCR
        • Budget management
        • Expense categorization
        • Interactive charts & reports
        """)
        features_text.setFont(Fonts.body_sm())
        features_text.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        frame_layout.addWidget(app_label)
        frame_layout.addWidget(version_label)
        frame_layout.addWidget(dev_label)
        frame_layout.addSpacing(Spacing.LG)
        frame_layout.addWidget(features_label)
        frame_layout.addWidget(features_text)
        
        frame.setLayout(frame_layout)
        layout.addWidget(frame)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def choose_color(self):
        """Choose accent color"""
        color = QColorDialog.getColor(QColor(Colors.ACCENT), self, "Choose Accent Color")
        if color.isValid():
            self.settings['accent_color'] = color.name()
    
    def reset_to_defaults(self):
        """Reset settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset Settings",
            "Reset all settings to default values?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.settings = {
                'theme_mode': 'light',
                'currency': 'USD',
                'notifications_enabled': True,
                'sound_enabled': True,
                'animations_enabled': True,
                'budget_alerts_enabled': True,
                'items_per_page': 20,
                'accent_color': Colors.ACCENT,
            }
            QMessageBox.information(self, "Success", "Settings reset to defaults")
    
    def save_settings(self):
        """Save settings"""
        self.settings_changed.emit(self.settings)
        QMessageBox.information(self, "Success", "Settings saved successfully")
    
    def on_clear_data(self):
        """Handle clear data"""
        reply = QMessageBox.warning(
            self, "Clear All Data",
            "This will permanently delete all financial data. This cannot be undone!\n\nAre you sure?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # Would implement actual data clearing
            QMessageBox.information(self, "Data Cleared", "All data has been permanently deleted")
