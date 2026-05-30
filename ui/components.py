"""
Reusable UI Components for fintech dashboard
Cards, buttons, inputs, and other building blocks
Premium Apple-inspired design with green + white theme
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QFrame, QGraphicsDropShadowEffect, QSpinBox, QDoubleSpinBox, QComboBox,
    QProgressBar, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap, QBrush, QPainter, QCursor
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSlice
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
    """Card for displaying a statistic with premium styling"""
    
    def __init__(self, title: str = "", value: str = "", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.layout.setSpacing(Spacing.SM)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setFont(Fonts.caption())
        self.title_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        # Value with proper color
        self.value_label = QLabel(value)
        self.value_label.setFont(Fonts.heading_4())
        self.value_label.setStyleSheet(f"color: {Colors.TEXT_MONEY_NEUTRAL}; font-weight: 700;")
        
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
        self.value_label.setStyleSheet(f"color: {color}; font-weight: 700;")


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
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaledToWidth(32, Qt.SmoothTransformation))
            top_layout.addWidget(icon_label)
        
        # Title and value
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(Spacing.XS)
        
        title_label = QLabel(title)
        title_label.setFont(Fonts.caption())
        title_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        value_label = QLabel(value)
        value_label.setFont(Fonts.heading_5())
        value_label.setStyleSheet(f"color: {color}; font-weight: 700;")
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(value_label)
        
        top_layout.addLayout(info_layout)
        top_layout.addStretch()
        
        self.layout.addLayout(top_layout)
        self.layout.addStretch()


# ============================================================================
# BUTTON COMPONENTS
# ============================================================================

class PrimaryButton(QPushButton):
    """Premium primary button with hover effects"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(44)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFont(Fonts.body_base())
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                padding: 10px 24px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.ACCENT_FOCUS};
            }}
            QPushButton:disabled {{
                background-color: {Colors.DISABLED};
                color: {Colors.TEXT_TERTIARY};
            }}
        """)


class SecondaryButton(QPushButton):
    """Secondary button with outline style"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(44)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFont(Fonts.body_base())
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 10px 24px;
                font-weight: 500;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
                border: 1px solid {Colors.ACCENT};
            }}
            QPushButton:pressed {{
                background-color: {Colors.FOCUS};
                border: 1px solid {Colors.ACCENT};
            }}
        """)


class GhostButton(QPushButton):
    """Ghost button with minimal style"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFont(Fonts.body_base())
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_PRIMARY};
                border: none;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {Colors.ACCENT};
            }}
            QPushButton:pressed {{
                color: {Colors.ACCENT_FOCUS};
            }}
        """)


# ============================================================================
# INPUT COMPONENTS
# ============================================================================

class PremiumLineEdit(QLineEdit):
    """Premium text input with enhanced styling"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(44)
        self.setFont(Fonts.body_base())
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 10px 12px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.ACCENT};
                background-color: {Colors.BG_SECONDARY};
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_TERTIARY};
            }}
        """)


class PremiumSpinBox(QDoubleSpinBox):
    """Premium numeric input"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(44)
        self.setFont(Fonts.body_base())
        self.setDecimals(2)
        self.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: 8px 12px;
                font-size: 14px;
            }}
            QDoubleSpinBox:focus {{
                border: 2px solid {Colors.ACCENT};
            }}
        """)


# ============================================================================
# LAYOUT COMPONENTS
# ============================================================================

class Section(QFrame):
    """Section container with optional title"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            Section {{
                background-color: transparent;
                border: none;
            }}
        """)
        
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
    
    def add_widget(self, widget):
        """Add widget to section"""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add layout to section"""
        self.content_layout.addLayout(layout)


class HSection(QFrame):
    """Horizontal section for side-by-side layouts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            HSection {{
                background-color: transparent;
                border: none;
            }}
        """)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(Spacing.LG)
        self.setLayout(self.layout)
    
    def add_widget(self, widget):
        """Add widget"""
        self.layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add layout"""
        self.layout.addLayout(layout)


class VSection(QFrame):
    """Vertical section"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            VSection {{
                background-color: transparent;
                border: none;
            }}
        """)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(Spacing.MD)
        self.setLayout(self.layout)
    
    def add_widget(self, widget):
        """Add widget"""
        self.layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add layout"""
        self.layout.addLayout(layout)


# ============================================================================
# PROGRESS COMPONENTS
# ============================================================================

class ProgressRing(QFrame):
    """Circular progress indicator"""
    
    def __init__(self, size: int = 100, value: float = 0.5, color: str = Colors.ACCENT, parent=None):
        super().__init__(parent)
        self.size = size
        self.value = value
        self.color = color
        self.setFixedSize(size, size)
        self.setStyleSheet("background-color: transparent; border: none;")
    
    def setValue(self, value: float):
        """Set progress value (0-1)"""
        self.value = max(0, min(1, value))
        self.update()
    
    def paintEvent(self, event):
        """Paint circular progress"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center = self.size / 2
        radius = self.size / 2 - 5
        
        # Background circle
        painter.setPen(QColor(Colors.BORDER_LIGHT))
        painter.drawEllipse(center - radius, center - radius, radius * 2, radius * 2)
        
        # Progress arc
        painter.setPen(QColor(self.color))
        painter.drawArc(
            int(center - radius), int(center - radius),
            int(radius * 2), int(radius * 2),
            90 * 16, int(-self.value * 360 * 16)
        )


# ============================================================================
# TABLE COMPONENTS
# ============================================================================

class DataTable(QTableWidget):
    """Premium data table"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                gridline-color: {Colors.BORDER_LIGHT};
            }}
            QTableWidget::item {{
                padding: 8px 12px;
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: {Colors.HOVER};
                color: {Colors.TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                padding: 8px 12px;
                border: none;
                border-right: 1px solid {Colors.BORDER_LIGHT};
                font-weight: 600;
            }}
        """)
        
        # Style header
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        
        # Font
        self.setFont(Fonts.body_base())


# ============================================================================
# SEPARATOR COMPONENT
# ============================================================================

class Separator(QFrame):
    """Visual separator line"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        self.setStyleSheet(f"color: {Colors.BORDER_LIGHT};")
        self.setFixedHeight(1)


class VerticalSeparator(QFrame):
    """Vertical separator line"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        self.setStyleSheet(f"color: {Colors.BORDER_LIGHT};")
        self.setFixedWidth(1)


# ============================================================================
# SIDEBAR COMPONENTS
# ============================================================================

class SidebarItem(QPushButton):
    """Sidebar navigation item"""
    
    def __init__(self, name: str, icon_path: str = None, parent=None):
        super().__init__(parent)
        self.setText(name)
        self.setMinimumHeight(44)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFont(Fonts.body_base())
        
        # Icon
        if icon_path and os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))
        
        self.setStyleSheet(f"""
            SidebarItem {{
                background-color: transparent;
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid transparent;
                border-radius: {BorderRadius.MD}px;
                padding: 8px 12px;
                text-align: left;
                font-weight: 500;
            }}
            SidebarItem:hover {{
                background-color: {Colors.HOVER};
                border: 1px solid {Colors.BORDER_LIGHT};
            }}
            SidebarItem:pressed {{
                background-color: {Colors.ACCENT};
                color: white;
                border: 1px solid {Colors.ACCENT};
            }}
        """)


import os



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
                background-color: {Colors.ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.ACCENT_FOCUS};
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
                background-color: {Colors.HOVER};
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
