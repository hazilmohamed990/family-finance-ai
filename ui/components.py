"""
Reusable UI Components for fintech dashboard
Cards, buttons, inputs, and other building blocks
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QFrame, QGraphicsDropShadowEffect, QSpinBox, QDoubleSpinBox, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from .theme import Colors, Fonts, Spacing, BorderRadius, Shadows


# ============================================================================
# CARD COMPONENTS
# ============================================================================

class Card(QFrame):
    """Floating card with shadow and rounded corners"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet(f"""
            Card {{
                background-color: {Colors.BG_SECONDARY};
                border-radius: {BorderRadius.LG}px;
                border: 1px solid {Colors.BORDER_LIGHT};
            }}
        """)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        self.layout.setSpacing(Spacing.MD)
        self.setLayout(self.layout)


class StatCard(Card):
    """Card for displaying a statistic"""
    
    def __init__(self, title: str = "", value: str = "", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.layout.setSpacing(Spacing.SM)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setFont(Fonts.caption())
        self.title_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setFont(Fonts.heading_4())
        self.value_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        # Subtitle
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setFont(Fonts.body_xs())
        self.subtitle_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY};")
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.value_label)
        if subtitle:
            self.layout.addWidget(self.subtitle_label)
        self.layout.addStretch()
    
    def set_value(self, value: str):
        """Update the value"""
        self.value_label.setText(value)
    
    def set_title(self, title: str):
        """Update the title"""
        self.title_label.setText(title)
    
    def set_accent_color(self, color: str):
        """Set accent color for the value"""
        self.value_label.setStyleSheet(f"color: {color};")


class MetricCard(Card):
    """Card with metric display and optional icon"""
    
    def __init__(self, title: str, value: str, icon_path: str = None, color: str = Colors.ACCENT, parent=None):
        super().__init__(parent)
        self.layout.setSpacing(Spacing.MD)
        
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Icon
        if icon_path:
            icon_label = QLabel()
            pixmap = QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            top_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(Fonts.label_small())
        title_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        top_layout.addStretch()
        top_layout.addWidget(title_label)
        
        self.layout.addLayout(top_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(Fonts.heading_3())
        value_label.setStyleSheet(f"color: {color};")
        self.layout.addWidget(value_label)


class InfoCard(Card):
    """Card for displaying information with title and content"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        
        # Title
        if title:
            title_label = QLabel(title)
            title_label.setFont(Fonts.heading_5())
            title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            self.layout.addWidget(title_label)
        
        # Content area
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(Spacing.SM)
        self.layout.addLayout(self.content_layout)
    
    def add_content(self, widget: QWidget):
        """Add content to the info card"""
        self.content_layout.addWidget(widget)


# ============================================================================
# BUTTON COMPONENTS
# ============================================================================

class PrimaryButton(QPushButton):
    """Primary action button"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                padding: 10px 18px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {Colors.FOCUS};
            }}
            QPushButton:pressed {{
                background-color: #0284C7;
            }}
            QPushButton:disabled {{
                background-color: {Colors.DISABLED};
                color: {Colors.TEXT_TERTIARY};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)


class SecondaryButton(QPushButton):
    """Secondary action button"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 10px 18px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
            QPushButton:pressed {{
                background-color: #E0E7FF;
            }}
            QPushButton:disabled {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_TERTIARY};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)


class DangerButton(QPushButton):
    """Destructive action button"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ERROR};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                padding: 10px 18px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #DC2626;
            }}
            QPushButton:pressed {{
                background-color: #B91C1C;
            }}
            QPushButton:disabled {{
                background-color: {Colors.DISABLED};
                color: {Colors.TEXT_TERTIARY};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)


class SuccessButton(QPushButton):
    """Success action button"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.SUCCESS};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                padding: 10px 18px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
            QPushButton:pressed {{
                background-color: #047857;
            }}
            QPushButton:disabled {{
                background-color: {Colors.DISABLED};
                color: {Colors.TEXT_TERTIARY};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)


class IconButton(QPushButton):
    """Icon-only button with minimal styling"""
    
    def __init__(self, icon_path: str = "", size: int = 24, parent=None):
        super().__init__(parent)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(size, size))
        self.setFixedSize(size + 12, size + 12)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {BorderRadius.SM}px;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_TERTIARY};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)


# ============================================================================
# INPUT COMPONENTS
# ============================================================================

class StyledLineEdit(QLineEdit):
    """Premium styled line edit"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 10px 12px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {Colors.ACCENT};
                background-color: {Colors.BG_SECONDARY};
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_TERTIARY};
            }}
        """)
        self.setMinimumHeight(40)


class AmountInput(QDoubleSpinBox):
    """Specialized input for currency amounts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 8px 12px;
                font-size: 13px;
            }}
            QDoubleSpinBox:focus {{
                border: 1px solid {Colors.ACCENT};
            }}
        """)
        self.setMinimum(0)
        self.setMaximum(999999.99)
        self.setDecimals(2)
        self.setMinimumHeight(40)
        self.setCorrectionMode(QDoubleSpinBox.CorrectToNearestValue)


class StyledComboBox(QComboBox):
    """Premium styled combo box"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 8px 12px;
                font-size: 13px;
            }}
            QComboBox:focus {{
                border: 1px solid {Colors.ACCENT};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                selection-background-color: {Colors.ACCENT};
            }}
        """)
        self.setMinimumHeight(40)


# ============================================================================
# LAYOUT HELPERS
# ============================================================================

class HSection(QWidget):
    """Horizontal section with title and content"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.MD)
        
        if title:
            title_label = QLabel(title)
            title_label.setFont(Fonts.heading_5())
            title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            layout.addWidget(title_label)
        
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(Spacing.LG)
        layout.addLayout(self.content_layout)
        
        self.setLayout(layout)


class VSection(QWidget):
    """Vertical section with title and content"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.MD)
        
        if title:
            title_label = QLabel(title)
            title_label.setFont(Fonts.heading_5())
            title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            layout.addWidget(title_label)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(Spacing.MD)
        layout.addLayout(self.content_layout)
        
        self.setLayout(layout)


# ============================================================================
# SIDEBAR COMPONENTS
# ============================================================================

class SidebarItem(QPushButton):
    """Sidebar navigation item"""
    
    def __init__(self, text: str, icon_path: str = "", parent=None):
        super().__init__(parent)
        self.setText(text)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(20, 20))
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: none;
                border-radius: {BorderRadius.SM}px;
                padding: 10px 12px;
                text-align: left;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(44)
    
    def set_active(self, active: bool):
        """Set active state"""
        if active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.ACCENT};
                    color: white;
                    border: none;
                    border-radius: {BorderRadius.SM}px;
                    padding: 10px 12px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: 600;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Colors.TEXT_SECONDARY};
                    border: none;
                    border-radius: {BorderRadius.SM}px;
                    padding: 10px 12px;
                    text-align: left;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.HOVER};
                    color: {Colors.TEXT_PRIMARY};
                }}
            """)


# ============================================================================
# SEPARATOR
# ============================================================================

class Separator(QFrame):
    """Horizontal separator line"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        self.setStyleSheet(f"background-color: {Colors.BORDER_LIGHT};")
        self.setFixedHeight(1)
