"""
Premium Fintech Theme System - Apple-Inspired Green + White
Production-ready theme for premium fintech applications
Forces SF Pro font globally with macOS aesthetics
"""

from PyQt5.QtGui import QFont, QColor, QFontDatabase
from PyQt5.QtCore import Qt
import os

# ============================================================================
# FONT SYSTEM - GLOBAL SF PRO INTEGRATION
# ============================================================================

class FontManager:
    """Manages SF Pro font loading and ensures global application"""
    
    FONT_PATH = "assets/fonts/SF-Pro.ttf"
    FONT_FAMILY = None
    _font_id = None
    
    @staticmethod
    def load_font():
        """Load SF Pro font globally and record family name"""
        if FontManager._font_id is None:
            if os.path.exists(FontManager.FONT_PATH):
                FontManager._font_id = QFontDatabase.addApplicationFont(FontManager.FONT_PATH)
                if FontManager._font_id != -1:
                    font_families = QFontDatabase.applicationFontFamilies(FontManager._font_id)
                    if font_families:
                        FontManager.FONT_FAMILY = font_families[0]
                        return True
            return False
        return True

# ============================================================================
# COLOR PALETTE - PREMIUM GREEN + WHITE FINTECH THEME
# ============================================================================

class Colors:
    # PRIMARY GREENS - Apple-Inspired Fintech
    GREEN_PRIMARY = "#00A876"      # Primary action green (premium, bold)
    GREEN_SECONDARY = "#06B078"    # Secondary green (slightly lighter)
    GREEN_LIGHT = "#34C759"        # Light green (accent)
    GREEN_ULTRA_LIGHT = "#D1FAE5"  # Ultra light (backgrounds)
    
    # DARK GREENS - Premium text and accents
    GREEN_DARK = "#065F46"         # Deep forest green (dark mode friendly)
    GREEN_DARKER = "#041E1A"       # Ultra dark green (text alternative)
    
    # SEMANTIC GREENS
    SUCCESS = "#10B981"             # Success/positive indicator
    INCOME = "#06B078"              # Income - green theme
    SAVINGS = "#00A876"             # Savings - primary green
    
    # FINANCIAL INDICATORS
    EXPENSE = "#DC2626"             # Expense - red (important)
    WARNING = "#F59E0B"             # Warning - amber
    ALERT = "#EF4444"               # Alert - red
    ERROR = ALERT
    INFO = "#10B981"
    
    # BACKGROUNDS
    BG_PRIMARY = "#FAFBFC"          # Soft white background
    BG_SECONDARY = "#FFFFFF"        # Card/panel white
    BG_TERTIARY = "#F3F4F6"         # Subtle background
    BG_HOVER = "#E8F5E9"            # Green hover state
    
    # TEXT COLORS - High contrast for readability
    TEXT_PRIMARY = "#0F172A"        # Deep navy-black (highest contrast)
    TEXT_SECONDARY = "#475569"      # Medium gray
    TEXT_TERTIARY = "#94A3B8"       # Light gray
    TEXT_LIGHT = "#E2E8F0"          # Very light gray
    TEXT_INVERSE = "#FFFFFF"        # Inverse (white on dark)
    
    # FINANCIAL TEXT - High visibility
    TEXT_MONEY_POSITIVE = "#00A876" # Positive money (green)
    TEXT_MONEY_NEGATIVE = "#DC2626" # Negative money (red)
    TEXT_MONEY_NEUTRAL = "#0F172A"  # Neutral money (dark)
    
    # INTERACTIVE
    ACCENT = "#00A876"              # Primary accent (green)
    ACCENT_HOVER = "#00824D"        # Hover state (darker green)
    ACCENT_FOCUS = "#005C3D"        # Focus state (even darker)
    HOVER = "#D1FAE5"               # Hover background (light green)
    FOCUS = "#A7F3D0"               # Focus background (medium light green)
    DISABLED = "#D1D5DB"            # Disabled state
    
    # BORDERS
    BORDER_LIGHT = "#E5E7EB"        # Light border
    BORDER_MEDIUM = "#D1D5DB"       # Medium border
    BORDER_DARK = "#9CA3AF"         # Dark border
    
    # SHADOWS & OVERLAYS
    SHADOW_COLOR = "#000000"        # Shadow color
    OVERLAY_LIGHT = "rgba(0, 168, 118, 0.05)"  # Light green overlay
    OVERLAY_MEDIUM = "rgba(0, 168, 118, 0.1)"  # Medium green overlay
    
    # CHART COLORS - Green-based palette
    CHART_1 = "#00A876"             # Primary green
    CHART_2 = "#34C759"             # Light green
    CHART_3 = "#10B981"             # Emerald
    CHART_4 = "#06B078"             # Secondary green
    CHART_5 = "#00824D"             # Dark green
    CHART_6 = "#D1FAE5"             # Ultra light green


class Shadows:
    """Shadow styles for depth"""
    SHADOW_NONE = "0px 0px 0px rgba(0, 0, 0, 0);"
    SHADOW_SM = "0px 1px 2px rgba(0, 0, 0, 0.05);"
    SHADOW_BASE = "0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06);"
    SHADOW_MD = "0px 4px 6px rgba(0, 0, 0, 0.07), 0px 2px 4px rgba(0, 0, 0, 0.06);"
    SHADOW_LG = "0px 10px 15px rgba(0, 0, 0, 0.1), 0px 4px 6px rgba(0, 0, 0, 0.05);"
    SHADOW_XL = "0px 20px 25px rgba(0, 0, 0, 0.1), 0px 10px 10px rgba(0, 0, 0, 0.04);"


class Spacing:
    """Consistent spacing system"""
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24
    XXXL = 32
    HUGE = 40


class BorderRadius:
    """Border radius values"""
    NONE = 0
    SM = 6
    MD = 8
    LG = 12
    XL = 16
    FULL = 24


# ============================================================================
# TYPOGRAPHY
# ============================================================================

class Fonts:
    """Font configurations"""
    
    FAMILY_PRIMARY = "SF Pro"
    FAMILY_FALLBACK = "Segoe UI"
    
    @staticmethod
    def get_font(size: int, weight: int = QFont.Normal, italic: bool = False) -> QFont:
        """Get configured font (uses loaded SF Pro when available)"""
        family = FontManager.FONT_FAMILY or Fonts.FAMILY_PRIMARY or Fonts.FAMILY_FALLBACK
        font = QFont(family, size)
        font.setWeight(weight)
        font.setItalic(italic)
        return font
    
    # Heading styles
    @staticmethod
    def heading_1() -> QFont:
        return Fonts.get_font(32, QFont.Bold)
    
    @staticmethod
    def heading_2() -> QFont:
        return Fonts.get_font(26, QFont.Bold)
    
    @staticmethod
    def heading_3() -> QFont:
        return Fonts.get_font(22, QFont.Bold)
    
    @staticmethod
    def heading_4() -> QFont:
        return Fonts.get_font(18, QFont.DemiBold)
    
    @staticmethod
    def heading_5() -> QFont:
        return Fonts.get_font(16, QFont.DemiBold)
    
    # Body styles
    @staticmethod
    def body_lg() -> QFont:
        return Fonts.get_font(15, QFont.Normal)
    
    @staticmethod
    def body_base() -> QFont:
        return Fonts.get_font(14, QFont.Normal)
    
    @staticmethod
    def body_sm() -> QFont:
        return Fonts.get_font(13, QFont.Normal)
    
    @staticmethod
    def body_xs() -> QFont:
        return Fonts.get_font(12, QFont.Normal)
    
    # Label styles
    @staticmethod
    def label() -> QFont:
        return Fonts.get_font(13, QFont.Medium)
    
    @staticmethod
    def label_small() -> QFont:
        return Fonts.get_font(12, QFont.Medium)
    
    # Caption
    @staticmethod
    def caption() -> QFont:
        return Fonts.get_font(11, QFont.Normal)


# ============================================================================
# QSS STYLESHEET
# ============================================================================

GLOBAL_STYLESHEET = f"""
/* Main Application */
QMainWindow {{
    background-color: {Colors.BG_PRIMARY};
}}

QWidget {{
    background-color: {Colors.BG_PRIMARY};
    color: {Colors.TEXT_PRIMARY};
}}

/* Scrollbars */
QScrollBar:vertical {{
    background-color: {Colors.BG_TERTIARY};
    width: 8px;
    border: none;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background-color: {Colors.TEXT_TERTIARY};
    border-radius: 4px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {Colors.TEXT_SECONDARY};
}}

QScrollBar:horizontal {{
    background-color: {Colors.BG_TERTIARY};
    height: 8px;
    border: none;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal {{
    background-color: {Colors.TEXT_TERTIARY};
    border-radius: 4px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {Colors.TEXT_SECONDARY};
}}

/* Generic Button */
QPushButton {{
    background-color: {Colors.ACCENT};
    color: white;
    border: none;
    border-radius: {BorderRadius.MD}px;
    padding: 10px 16px;
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

/* Secondary Button */
QPushButton[style="secondary"] {{
    background-color: {Colors.BG_TERTIARY};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER_LIGHT};
}}

QPushButton[style="secondary"]:hover {{
    background-color: {Colors.HOVER};
}}

/* Text Input */
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

/* Text Edit */
QTextEdit {{
    background-color: {Colors.BG_SECONDARY};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: {BorderRadius.MD}px;
    padding: 10px 12px;
    font-size: 13px;
}}

QTextEdit:focus {{
    border: 1px solid {Colors.ACCENT};
}}

/* Combo Box */
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

/* Labels */
QLabel {{
    color: {Colors.TEXT_PRIMARY};
    font-family: 'SF Pro', 'Segoe UI', sans-serif;
}}

/* Group Box */
QGroupBox {{
    background-color: transparent;
    border: none;
    padding: 0px;
    color: {Colors.TEXT_PRIMARY};
    font-family: 'SF Pro', 'Segoe UI', sans-serif;
}}

/* Message Box */
QMessageBox {{
    background-color: {Colors.BG_PRIMARY};
}}

QMessageBox QLabel {{
    color: {Colors.TEXT_PRIMARY};
}}

QMessageBox QPushButton {{
    min-width: 60px;
}}

/* Table Widget */
QTableWidget, QTableView {{
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

/* Spin Box */
QSpinBox, QDoubleSpinBox {{
    background-color: {Colors.BG_SECONDARY};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: {BorderRadius.MD}px;
    padding: 8px 12px;
    font-size: 13px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1px solid {Colors.ACCENT};
}}

/* Check Box */
QCheckBox {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 13px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: {BorderRadius.SM}px;
    background-color: {Colors.BG_SECONDARY};
}}

QCheckBox::indicator:hover {{
    border: 1px solid {Colors.ACCENT};
    background-color: {Colors.HOVER};
}}

QCheckBox::indicator:checked {{
    background-color: {Colors.ACCENT};
    border: 1px solid {Colors.ACCENT};
}}

/* Radio Button */
QRadioButton {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 13px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 1px solid {Colors.BORDER_LIGHT};
    background-color: {Colors.BG_SECONDARY};
}}

QRadioButton::indicator:hover {{
    border: 1px solid {Colors.ACCENT};
    background-color: {Colors.HOVER};
}}

QRadioButton::indicator:checked {{
    background-color: {Colors.ACCENT};
    border: 1px solid {Colors.ACCENT};
}}

/* Dialog */
QDialog {{
    background-color: {Colors.BG_PRIMARY};
}}

/* File Dialog */
QFileDialog {{
    background-color: {Colors.BG_PRIMARY};
}}

/* Menu */
QMenu {{
    background-color: {Colors.BG_SECONDARY};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: {BorderRadius.MD}px;
    padding: {Spacing.SM}px 0px;
}}

QMenu::item:selected {{
    background-color: {Colors.HOVER};
    color: {Colors.TEXT_PRIMARY};
}}

/* Tab Widget */
QTabWidget::pane {{
    border: 1px solid {Colors.BORDER_LIGHT};
    background-color: {Colors.BG_SECONDARY};
}}

QTabBar::tab {{
    background-color: {Colors.BG_TERTIARY};
    color: {Colors.TEXT_PRIMARY};
    padding: 8px 16px;
    margin: 2px;
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: {BorderRadius.MD}px;
}}

QTabBar::tab:selected {{
    background-color: {Colors.ACCENT};
    color: white;
    border: 1px solid {Colors.ACCENT};
}}

QTabBar::tab:hover {{
    background-color: {Colors.HOVER};
}}

/* Slider */
QSlider::groove:horizontal {{
    background-color: {Colors.BG_TERTIARY};
    border-radius: 4px;
    height: 6px;
}}

QSlider::handle:horizontal {{
    background-color: {Colors.ACCENT};
    border: 2px solid {Colors.ACCENT};
    width: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background-color: {Colors.ACCENT_HOVER};
    border: 2px solid {Colors.ACCENT_HOVER};
}}

/* Progress Bar */
QProgressBar {{
    background-color: {Colors.BG_TERTIARY};
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: {BorderRadius.MD}px;
    text-align: center;
    color: {Colors.TEXT_PRIMARY};
}}

QProgressBar::chunk {{
    background-color: {Colors.ACCENT};
    border-radius: {BorderRadius.SM}px;
}}
"""


def get_color(color_name: str) -> QColor:
    """Get QColor from color name"""
    color_map = {
        'primary': Colors.TEXT_PRIMARY,
        'secondary': Colors.TEXT_SECONDARY,
        'tertiary': Colors.TEXT_TERTIARY,
        'accent': Colors.ACCENT,
        'income': Colors.INCOME,
        'expense': Colors.EXPENSE,
        'savings': Colors.SAVINGS,
        'success': Colors.SUCCESS,
        'warning': Colors.WARNING,
        'error': Colors.ERROR,
        'info': Colors.INFO,
    }
    return QColor(color_map.get(color_name, Colors.ACCENT))
