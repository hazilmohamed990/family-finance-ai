"""
Premium Fintech Theme System
Inspired by modern fintech dashboards and macOS aesthetics
"""

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

# ============================================================================
# COLOR PALETTE
# ============================================================================

class Colors:
    # Backgrounds
    BG_PRIMARY = "#FAFBFC"  # Soft white background
    BG_SECONDARY = "#FFFFFF"  # Card/panel white
    BG_TERTIARY = "#F5F7FA"  # Subtle background
    
    # Text
    TEXT_PRIMARY = "#1A1F2E"  # Deep charcoal
    TEXT_SECONDARY = "#6B7280"  # Medium gray
    TEXT_TERTIARY = "#9CA3AF"  # Light gray
    TEXT_LIGHT = "#E5E7EB"  # Very light gray
    
    # Semantic Colors
    INCOME = "#10B981"  # Emerald green
    EXPENSE = "#EF4444"  # Red
    SAVINGS = "#3B82F6"  # Blue
    NEUTRAL = "#8B5CF6"  # Purple
    
    # Charts
    CHART_1 = "#3B82F6"  # Blue
    CHART_2 = "#10B981"  # Green
    CHART_3 = "#F59E0B"  # Amber
    CHART_4 = "#EF4444"  # Red
    CHART_5 = "#8B5CF6"  # Purple
    CHART_6 = "#EC4899"  # Pink
    
    # Interactive
    ACCENT = "#3B82F6"  # Primary accent
    HOVER = "#E0F2FE"  # Hover state
    FOCUS = "#0EA5E9"  # Focus state
    DISABLED = "#D1D5DB"  # Disabled state
    
    # Status
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    ERROR = "#EF4444"
    INFO = "#3B82F6"
    
    # Borders
    BORDER_LIGHT = "#E5E7EB"
    BORDER_MEDIUM = "#D1D5DB"


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
    def get_font(size: int, weight: int = QFont.Bold, italic: bool = False) -> QFont:
        """Get configured font"""
        font = QFont(Fonts.FAMILY_PRIMARY, size)
        font.setFamily(Fonts.FAMILY_FALLBACK)
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
    background-color: {Colors.FOCUS};
}}

QPushButton:pressed {{
    background-color: #0284C7;
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
}}

/* Group Box */
QGroupBox {{
    background-color: transparent;
    border: none;
    padding: 0px;
    color: {Colors.TEXT_PRIMARY};
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
