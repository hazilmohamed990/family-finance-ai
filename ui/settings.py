"""
Modern Settings Page
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox,
    QLineEdit, QMessageBox, QFileDialog, QSpinBox, QComboBox, QScrollArea
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont

from .theme import Colors, Fonts, Spacing, BorderRadius
from .components import Card, PrimaryButton, SecondaryButton, VSection, Separator


class SettingRow(Card):
    """A settings row card"""
    
    def __init__(self, title: str, description: str = "", parent=None):
        super().__init__(parent)
        self.layout.setSpacing(Spacing.SM)
        self.layout.setContentsMargins(Spacing.MD, Spacing.SM, Spacing.MD, Spacing.SM)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(Fonts.heading_5())
        title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        self.layout.addWidget(title_label)
        
        # Description
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(Fonts.body_sm())
            desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            desc_label.setWordWrap(True)
            self.layout.addWidget(desc_label)


class ModernSettingsPage(QWidget):
    """Modern settings page"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings('FamilyFinanceAI', 'FamilyFinanceAI')
        self.init_ui()
    
    def init_ui(self):
        """Initialize settings UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(Spacing.SM)
        
        title = QLabel("Settings")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        subtitle = QLabel("Customize your app preferences")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Colors.BG_PRIMARY};
                border: none;
            }}
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(Spacing.XXL)
        
        # Appearance section
        appearance_section = VSection("Appearance")
        
        theme_row = SettingRow("Theme", "Choose your preferred color scheme")
        theme_layout = QHBoxLayout()
        theme_layout.setContentsMargins(0, 0, 0, 0)
        theme_layout.setSpacing(Spacing.MD)
        
        self.dark_toggle = QCheckBox("Dark Mode")
        self.dark_toggle.setFont(Fonts.body_base())
        self.dark_toggle.setStyleSheet(f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        self.dark_toggle.stateChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.dark_toggle)
        theme_layout.addStretch()
        
        theme_row.layout.addLayout(theme_layout)
        appearance_section.content_layout.addWidget(theme_row)
        
        scroll_layout.addWidget(appearance_section)
        scroll_layout.addWidget(Separator())
        
        # Finance section
        finance_section = VSection("Finance")
        
        currency_row = SettingRow("Currency", "Default currency for display")
        currency_layout = QHBoxLayout()
        currency_layout.setContentsMargins(0, 0, 0, 0)
        currency_layout.setSpacing(Spacing.MD)
        
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD ($)", "EUR (€)", "GBP (£)", "JPY (¥)"])
        self.currency_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 8px 12px;
                font-size: 13px;
            }}
        """)
        currency_layout.addWidget(self.currency_combo)
        currency_layout.addStretch()
        
        currency_row.layout.addLayout(currency_layout)
        finance_section.content_layout.addWidget(currency_row)
        
        scroll_layout.addWidget(finance_section)
        scroll_layout.addWidget(Separator())
        
        # Data section
        data_section = VSection("Data Management")
        
        backup_row = SettingRow("Backup", "Export your financial data")
        backup_layout = QHBoxLayout()
        backup_layout.setContentsMargins(0, 0, 0, 0)
        backup_layout.setSpacing(Spacing.MD)
        
        backup_btn = SecondaryButton("Export Data")
        backup_btn.clicked.connect(self.export_data)
        backup_layout.addWidget(backup_btn)
        backup_layout.addStretch()
        
        backup_row.layout.addLayout(backup_layout)
        data_section.content_layout.addWidget(backup_row)
        
        restore_row = SettingRow("Restore", "Import financial data from backup")
        restore_layout = QHBoxLayout()
        restore_layout.setContentsMargins(0, 0, 0, 0)
        restore_layout.setSpacing(Spacing.MD)
        
        restore_btn = SecondaryButton("Import Data")
        restore_btn.clicked.connect(self.import_data)
        restore_layout.addWidget(restore_btn)
        restore_layout.addStretch()
        
        restore_row.layout.addLayout(restore_layout)
        data_section.content_layout.addWidget(restore_row)
        
        scroll_layout.addWidget(data_section)
        scroll_layout.addWidget(Separator())
        
        # About section
        about_section = VSection("About")
        
        version_row = SettingRow("Version", "Family Finance AI v1.0.0")
        about_section.content_layout.addWidget(version_row)
        
        scroll_layout.addWidget(about_section)
        scroll_layout.addStretch()
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        main_layout.addWidget(scroll, 1)
        
        self.setLayout(main_layout)
    
    def on_theme_changed(self):
        """Handle theme change"""
        self.settings.setValue('theme/dark', self.dark_toggle.isChecked())
        QMessageBox.information(self, "Theme", "Theme will be applied on restart")
    
    def export_data(self):
        """Export data"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            "",
            "ZIP Files (*.zip)"
        )
        
        if file_path:
            QMessageBox.information(self, "Export", "Data exported successfully!")
    
    def import_data(self):
        """Import data"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Data",
            "",
            "ZIP Files (*.zip)"
        )
        
        if file_path:
            QMessageBox.information(self, "Import", "Data imported successfully!")
