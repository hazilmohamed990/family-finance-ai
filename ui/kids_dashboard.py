"""
Kids Dashboard - Child-friendly, gamified financial interface
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGridLayout, QScrollArea, QFrame, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice

from database.enhanced_db import EnhancedDatabase
from ui.theme import Colors, Fonts, Spacing, BorderRadius


class PiggyBankWidget(QWidget):
    """Animated virtual piggy bank display"""
    
    def __init__(self, savings_amount: float = 0, parent=None):
        super().__init__(parent)
        self.savings_amount = savings_amount
        self.init_ui()
        self.animate_value()
    
    def init_ui(self):
        """Initialize piggy bank UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        layout.setSpacing(Spacing.LG)
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel("My Piggy Bank")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        title.setAlignment(Qt.AlignCenter)
        
        # Piggy bank emoji/icon
        piggy = QLabel("🐷")
        piggy.setFont(QFont("Arial", 120))
        piggy.setAlignment(Qt.AlignCenter)
        
        # Amount display
        self.amount_label = QLabel(f"${self.savings_amount:.2f}")
        self.amount_label.setFont(QFont(Fonts.FAMILY_PRIMARY, 64, QFont.Bold))
        self.amount_label.setStyleSheet(f"color: {Colors.SAVINGS};")
        self.amount_label.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Total Saved")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        subtitle.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addSpacing(Spacing.LG)
        layout.addWidget(piggy)
        layout.addSpacing(Spacing.LG)
        layout.addWidget(self.amount_label)
        layout.addWidget(subtitle)
        layout.addStretch()
        
        # Frame styling
        frame = QFrame()
        frame.setLayout(layout)
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E0F2FE, stop:1 #F0FFFE);
                border-radius: {BorderRadius.XL}px;
                border: 2px solid {Colors.SAVINGS};
            }}
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)
    
    def animate_value(self):
        """Animate value increase"""
        pass  # Animation can be enhanced later
    
    def update_savings(self, amount: float):
        """Update savings amount"""
        self.savings_amount = amount
        self.amount_label.setText(f"${amount:.2f}")


class AchievementBadge(QFrame):
    """Individual achievement badge"""
    
    def __init__(self, badge_name: str, description: str = "", icon: str = "🏆", 
                 color: str = "#F59E0B", parent=None):
        super().__init__(parent)
        self.badge_name = badge_name
        self.description = description
        self.icon = icon
        self.color = color
        self.init_ui()
    
    def init_ui(self):
        """Initialize badge UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        layout.setSpacing(Spacing.SM)
        layout.setAlignment(Qt.AlignCenter)
        
        # Badge icon
        icon_label = QLabel(self.icon)
        icon_label.setFont(QFont("Arial", 40))
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Badge name
        name_label = QLabel(self.badge_name)
        name_label.setFont(Fonts.body_sm())
        name_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: bold;")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        
        if self.description:
            desc_label = QLabel(self.description)
            desc_label.setFont(Fonts.caption())
            desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        self.setLayout(layout)
        self.setMinimumSize(120, 140)
        
        # Styling
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {self.color};
                border-radius: {BorderRadius.LG}px;
            }}
        """)


class PointsDisplay(QFrame):
    """Display current points"""
    
    def __init__(self, points: int = 0, parent=None):
        super().__init__(parent)
        self.points = points
        self.init_ui()
    
    def init_ui(self):
        """Initialize points display"""
        layout = QHBoxLayout()
        layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        layout.setSpacing(Spacing.MD)
        
        # Star icon
        star_label = QLabel("⭐")
        star_label.setFont(QFont("Arial", 32))
        
        # Points text
        points_layout = QVBoxLayout()
        
        points_value = QLabel(str(self.points))
        points_value.setFont(QFont(Fonts.FAMILY_PRIMARY, 28, QFont.Bold))
        points_value.setStyleSheet(f"color: {Colors.WARNING};")
        
        points_label = QLabel("Points")
        points_label.setFont(Fonts.body_sm())
        points_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        points_layout.addWidget(points_value)
        points_layout.addWidget(points_label)
        
        layout.addWidget(star_label)
        layout.addLayout(points_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Styling
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
        """)


class SavingsGoalCard(QFrame):
    """Display savings goal with progress"""
    
    def __init__(self, goal_name: str, target_amount: float, current_amount: float = 0, 
                 icon: str = "🎯", deadline: str = None, parent=None):
        super().__init__(parent)
        self.goal_name = goal_name
        self.target_amount = target_amount
        self.current_amount = current_amount
        self.icon = icon
        self.deadline = deadline
        self.init_ui()
    
    def init_ui(self):
        """Initialize goal card"""
        layout = QVBoxLayout()
        layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        layout.setSpacing(Spacing.MD)
        
        # Top row - icon and name
        top_layout = QHBoxLayout()
        icon_label = QLabel(self.icon)
        icon_label.setFont(QFont("Arial", 28))
        
        name_label = QLabel(self.goal_name)
        name_label.setFont(Fonts.body_base())
        name_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: bold;")
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(name_label)
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
        # Progress bar
        progress = QProgressBar()
        progress.setMaximum(100)
        percentage = int((self.current_amount / self.target_amount * 100) if self.target_amount > 0 else 0)
        progress.setValue(min(percentage, 100))
        progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: {BorderRadius.SM}px;
                background-color: {Colors.BG_TERTIARY};
                text-align: center;
                height: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.SAVINGS};
                border-radius: {BorderRadius.SM}px;
            }}
        """)
        layout.addWidget(progress)
        
        # Amount display
        amount_layout = QHBoxLayout()
        current_label = QLabel(f"${self.current_amount:.2f}")
        current_label.setFont(Fonts.body_sm())
        current_label.setStyleSheet(f"color: {Colors.SAVINGS}; font-weight: bold;")
        
        target_label = QLabel(f"of ${self.target_amount:.2f}")
        target_label.setFont(Fonts.body_xs())
        target_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        amount_layout.addWidget(current_label)
        amount_layout.addWidget(target_label)
        amount_layout.addStretch()
        layout.addLayout(amount_layout)
        
        # Deadline if exists
        if self.deadline:
            deadline_label = QLabel(f"By {self.deadline}")
            deadline_label.setFont(Fonts.caption())
            deadline_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY};")
            layout.addWidget(deadline_label)
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
        """)
    
    def update_progress(self, current_amount: float):
        """Update goal progress"""
        self.current_amount = current_amount
        self.init_ui()  # Refresh


class SpendingEducationWidget(QFrame):
    """Financial education tips for kids"""
    
    def __init__(self, tips: list = None, parent=None):
        super().__init__(parent)
        self.tips = tips or [
            ("💰", "Save First", "Save part of your allowance before spending"),
            ("🎯", "Set Goals", "Have a target of what you want to buy"),
            ("📊", "Track Spending", "Know where your money goes"),
            ("🎁", "Earn Rewards", "Good financial habits earn you points!"),
        ]
        self.current_tip = 0
        self.init_ui()
    
    def init_ui(self):
        """Initialize education widget"""
        layout = QVBoxLayout()
        layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        layout.setSpacing(Spacing.MD)
        
        title = QLabel("💡 Financial Tips")
        title.setFont(Fonts.heading_5())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        # Tip display
        self.tip_layout = QVBoxLayout()
        self.update_tip_display()
        layout.addLayout(self.tip_layout)
        
        # Navigation buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Spacing.MD)
        
        prev_btn = QPushButton("← Previous")
        prev_btn.setMinimumHeight(32)
        prev_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
        """)
        prev_btn.clicked.connect(self.prev_tip)
        
        next_btn = QPushButton("Next →")
        next_btn.setMinimumHeight(32)
        next_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
        """)
        next_btn.clicked.connect(self.next_tip)
        
        button_layout.addWidget(prev_btn)
        button_layout.addStretch()
        button_layout.addWidget(next_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
        """)
    
    def update_tip_display(self):
        """Update current tip display"""
        # Clear layout
        while self.tip_layout.count():
            item = self.tip_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        icon, title, description = self.tips[self.current_tip % len(self.tips)]
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 36))
        
        title_label = QLabel(title)
        title_label.setFont(Fonts.heading_5())
        title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        desc_label = QLabel(description)
        desc_label.setFont(Fonts.body_sm())
        desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        desc_label.setWordWrap(True)
        
        self.tip_layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        self.tip_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        self.tip_layout.addWidget(desc_label, alignment=Qt.AlignCenter)
    
    def next_tip(self):
        """Show next tip"""
        self.current_tip += 1
        self.update_tip_display()
    
    def prev_tip(self):
        """Show previous tip"""
        self.current_tip -= 1
        self.update_tip_display()


class KidsDashboard(QWidget):
    """Main kids dashboard - colorful, gamified interface"""
    
    def __init__(self, db: EnhancedDatabase, child_data: dict, parent=None):
        super().__init__(parent)
        self.db = db
        self.child_data = child_data
        self.child_id = child_data['id']
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize kids dashboard UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(Spacing.LG)
        
        welcome = QLabel(f"Hi {self.child_data['name']}! 👋")
        welcome.setFont(Fonts.heading_2())
        welcome.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        header_layout.addWidget(welcome)
        header_layout.addStretch()
        
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
        
        # Top row - Piggy bank and Points
        top_row = QHBoxLayout()
        top_row.setSpacing(Spacing.LG)
        
        self.piggy_bank = PiggyBankWidget(0)
        self.points_display = PointsDisplay(0)
        
        top_row.addWidget(self.piggy_bank, 3)
        top_row.addWidget(self.points_display, 1)
        
        scroll_layout.addLayout(top_row)
        
        # Achievements
        achievements_title = QLabel("🏆 My Achievements")
        achievements_title.setFont(Fonts.heading_3())
        achievements_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        scroll_layout.addWidget(achievements_title)
        
        achievements_grid = QGridLayout()
        achievements_grid.setSpacing(Spacing.MD)
        
        self.achievements_container = achievements_grid
        
        # Sample achievements
        sample_badges = [
            ("First Step", "Made your first transaction", "👶"),
            ("Saver", "Saved $50", "💎"),
            ("Goal Setter", "Created a savings goal", "🎯"),
        ]
        
        for i, (name, desc, icon) in enumerate(sample_badges):
            badge = AchievementBadge(name, desc, icon)
            achievements_grid.addWidget(badge, i // 3, i % 3)
        
        scroll_layout.addLayout(achievements_grid)
        
        # Savings goals
        goals_title = QLabel("🎯 My Savings Goals")
        goals_title.setFont(Fonts.heading_3())
        goals_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        scroll_layout.addWidget(goals_title)
        
        self.goals_container = QVBoxLayout()
        self.goals_container.setSpacing(Spacing.MD)
        
        scroll_layout.addLayout(self.goals_container)
        
        # Education
        education = SpendingEducationWidget()
        scroll_layout.addWidget(education)
        
        # Quick actions
        actions_title = QLabel("Actions")
        actions_title.setFont(Fonts.heading_3())
        actions_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        scroll_layout.addWidget(actions_title)
        
        actions_layout = QGridLayout()
        actions_layout.setSpacing(Spacing.MD)
        
        actions = [
            ("View Allowance", "See your allowance", "💵"),
            ("View Spending", "Track your expenses", "📊"),
            ("Redeem Points", "Use your points", "🎁"),
        ]
        
        for i, (title, desc, emoji) in enumerate(actions):
            btn = QPushButton(f"{emoji}\n{title}")
            btn.setMinimumHeight(80)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.BG_SECONDARY};
                    color: {Colors.TEXT_PRIMARY};
                    border: 1px solid {Colors.BORDER_LIGHT};
                    border-radius: {BorderRadius.MD}px;
                    font-weight: bold;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.HOVER};
                }}
            """)
            btn.setCursor(Qt.PointingHandCursor)
            actions_layout.addWidget(btn, i // 3, i % 3)
        
        scroll_layout.addLayout(actions_layout)
        scroll_layout.addStretch()
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
    
    def load_data(self):
        """Load child data"""
        # Get savings
        savings = self.db.get_child_savings(self.child_id)
        if savings:
            self.piggy_bank.update_savings(savings['current_balance'] or 0)
        
        # Get points
        points = self.db.get_total_points(self.child_id)
        self.points_display.points = points
        self.points_display.init_ui()
        
        # Get goals
        goals = self.db.get_savings_goals(self.child_id, include_completed=False)
        
        # Clear goals container
        while self.goals_container.count():
            item = self.goals_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not goals:
            no_goals = QLabel("No goals yet. Create one to get started!")
            no_goals.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            self.goals_container.addWidget(no_goals)
        else:
            for goal in goals:
                goal_card = SavingsGoalCard(
                    goal['goal_name'],
                    goal['target_amount'],
                    goal['current_amount'] or 0,
                    goal.get('icon', '🎯'),
                    goal.get('deadline', None)
                )
                self.goals_container.addWidget(goal_card)
