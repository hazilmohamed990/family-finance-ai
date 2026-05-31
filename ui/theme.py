"""
Premium Fintech Theme System - Apple-Inspired Dark Mode
Deep charcoal, graphite, and emerald accents for a premium fintech UX.
Forces SF Pro font globally with robust fallbacks and application integration.
"""

from PyQt5.QtGui import QFont, QColor, QFontDatabase
from PyQt5.QtCore import Qt, QByteArray
import os
import sys

# ============================================================================
# FONT SYSTEM - GLOBAL SF PRO INTEGRATION
# ============================================================================

class FontManager:
    """Manages SF Pro font loading and ensures global application.

    This loader tries the bundled `assets/fonts/SF-Pro.ttf` and falls back to
    common system fonts if necessary. Call `apply_to_app(app)` to enforce
    the loaded font on the QApplication instance.
    """

    FONT_PATH = os.path.join(os.path.dirname(sys.argv[0]) if getattr(sys, 'argv', None) else os.getcwd(), 'assets', 'fonts', 'SF-Pro.ttf')
    FONT_FAMILY = None
    _font_id = None

    @staticmethod
    def load_font():
        """Attempt to load the bundled SF Pro font. Returns True if a family is set."""
        if FontManager.FONT_FAMILY:
            return True

        # Try bundled path(s)
        candidates = [
            FontManager.FONT_PATH,
            os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'SF-Pro.ttf')
        ]

        for p in candidates:
            try:
                p = os.path.abspath(p)
                if os.path.exists(p):
                    fid = QFontDatabase.addApplicationFont(p)
                    if fid != -1:
                        families = QFontDatabase.applicationFontFamilies(fid)
                        if families:
                            FontManager._font_id = fid
                            FontManager.FONT_FAMILY = families[0]
                            return True
            except Exception:
                continue

        # Try reading raw data (more permissive on some platforms)
        try:
            with open(candidates[0], 'rb') as f:
                raw = f.read()
            if raw:
                fid = QFontDatabase.addApplicationFontFromData(QByteArray(raw))
                if fid != -1:
                    families = QFontDatabase.applicationFontFamilies(fid)
                    if families:
                        FontManager._font_id = fid
                        FontManager.FONT_FAMILY = families[0]
                        return True
        except Exception:
            pass

        # System fallbacks
        fallbacks = ['SF Pro', 'San Francisco', 'Helvetica Neue', 'Segoe UI', 'Arial']
        for fam in fallbacks:
            try:
                q = QFont(fam)
                if q.family():
                    FontManager.FONT_FAMILY = q.family()
                    return True
            except Exception:
                continue

        return False

    @staticmethod
    def apply_to_app(app):
        """Apply loaded font to `app`. Loads font first if needed."""
        if not FontManager.FONT_FAMILY:
            FontManager.load_font()
        if FontManager.FONT_FAMILY:
            font = QFont(FontManager.FONT_FAMILY)
            font.setStyleStrategy(QFont.PreferAntialias)
            app.setFont(font)
            return True
        return False


# ============================================================================
# COLOR PALETTE - PREMIUM DARK FINTECH THEME
# ============================================================================

class Colors:
    # Dark neutrals
    BG_PRIMARY = '#0B0F11'       # deep charcoal
    BG_SECONDARY = '#0F1315'     # panel
    BG_TERTIARY = '#15191B'      # card
    BG_ELEVATED = '#1B1F21'      # elevated surfaces

    # Accent - Emerald
    ACCENT = '#00C48C'
    ACCENT_HOVER = '#00A876'
    ACCENT_FOCUS = '#007A53'

    # Text
    TEXT_PRIMARY = '#E6F2EE'
    TEXT_SECONDARY = '#B8C6C0'
    TEXT_TERTIARY = '#88908C'
    TEXT_DISABLED = '#5C6461'

    # States
    SUCCESS = '#10B981'
    EXPENSE = '#FF6B6B'
    WARNING = '#F59E0B'
    ERROR = '#EF4444'

    # Borders
    BORDER_LIGHT = '#1E2628'
    BORDER_MEDIUM = '#232A2C'

    # Hover / disabled helpers
    HOVER = '#13221A'
    DISABLED = '#2A2F2F'

    # Charts
    CHART_1 = ACCENT
    CHART_2 = '#34D89A'
    CHART_3 = '#1AB57D'
    CHART_4 = '#068A57'
    CHART_5 = '#0F6A4F'


class Shadows:
    SHADOW_NONE = '0px 0px 0px rgba(0,0,0,0)'
    SHADOW_SM = '0px 1px 2px rgba(0,0,0,0.35)'
    SHADOW_MD = '0px 6px 18px rgba(0,0,0,0.6)'


class Spacing:
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24


class BorderRadius:
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
    FAMILY_FALLBACK = 'Segoe UI'

    @staticmethod
    def get_font(size: int, weight: int = QFont.Normal, italic: bool = False) -> QFont:
        fam = FontManager.FONT_FAMILY or Fonts.FAMILY_FALLBACK
        f = QFont(fam, size)
        f.setWeight(weight)
        f.setItalic(italic)
        f.setStyleStrategy(QFont.PreferAntialias)
        return f

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

    @staticmethod
    def label() -> QFont:
        return Fonts.get_font(13, QFont.Medium)

    @staticmethod
    def caption() -> QFont:
        return Fonts.get_font(11, QFont.Normal)


# ============================================================================
# QSS STYLESHEET
# ============================================================================

GLOBAL_STYLESHEET = f"""
/* Main Application - Premium Dark */
QMainWindow {{
    background-color: {Colors.BG_PRIMARY};
}}

QWidget {{
    background-color: {Colors.BG_PRIMARY};
    color: {Colors.TEXT_PRIMARY};
}}

QPushButton {{
    background-color: {Colors.ACCENT};
    color: {Colors.BG_PRIMARY};
    border: none;
    border-radius: {BorderRadius.MD}px;
    padding: 10px 16px;
    font-weight: 600;
    font-size: 13px;
}}

QPushButton:hover {{
    background-color: {Colors.ACCENT_HOVER};
}}

QLineEdit, QTextEdit, QComboBox {{
    background-color: {Colors.BG_TERTIARY};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER_MEDIUM};
    border-radius: {BorderRadius.MD}px;
    padding: 8px 12px;
}}

QLabel {{
    color: {Colors.TEXT_PRIMARY};
}}

QGroupBox {{
    background-color: transparent;
    color: {Colors.TEXT_PRIMARY};
}}

QMessageBox {{
    background-color: {Colors.BG_ELEVATED};
}}

QTableWidget, QTableView {{
    background-color: {Colors.BG_TERTIARY};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER_MEDIUM};
}}

QHeaderView::section {{
    background-color: {Colors.BG_ELEVATED};
    color: {Colors.TEXT_PRIMARY};
    padding: 8px 12px;
    border-right: 1px solid {Colors.BORDER_MEDIUM};
}}

QTabBar::tab:selected {{
    background-color: {Colors.ACCENT};
    color: {Colors.BG_PRIMARY};
}}

QProgressBar {{
    background-color: {Colors.BG_TERTIARY};
    border: 1px solid {Colors.BORDER_MEDIUM};
    border-radius: {BorderRadius.MD}px;
    color: {Colors.TEXT_PRIMARY};
}}

QProgressBar::chunk {{
    background-color: {Colors.ACCENT};
}}
"""
