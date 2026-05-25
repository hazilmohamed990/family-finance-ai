"""
AI Financial Advisor - Chat interface with modern message bubbles
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QScrollArea, QFrame, QTextEdit
)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon

from database.enhanced_db import EnhancedDatabase
from ui.theme import Colors, Fonts, Spacing, BorderRadius


class ChatBubble(QFrame):
    """Message bubble for chat"""
    
    def __init__(self, message: str, is_user: bool = True, parent=None):
        super().__init__(parent)
        self.message = message
        self.is_user = is_user
        self.init_ui()
    
    def init_ui(self):
        """Initialize bubble UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(Spacing.MD, Spacing.SM, Spacing.MD, Spacing.SM)
        layout.setSpacing(0)
        
        # Container layout
        container = QHBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        container.setSpacing(0)
        
        # Message label
        msg_label = QLabel(self.message)
        msg_label.setFont(Fonts.body_sm())
        msg_label.setWordWrap(True)
        msg_label.setMaximumWidth(500)
        
        if self.is_user:
            # User message - right aligned, blue background
            container.addStretch()
            
            bubble = QFrame()
            bubble_layout = QVBoxLayout()
            bubble_layout.setContentsMargins(Spacing.MD, Spacing.SM, Spacing.MD, Spacing.SM)
            bubble_layout.addWidget(msg_label)
            bubble.setLayout(bubble_layout)
            
            bubble.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.ACCENT};
                    border-radius: {BorderRadius.MD}px;
                }}
            """)
            
            msg_label.setStyleSheet("color: white;")
            
            container.addWidget(bubble)
        else:
            # AI message - left aligned, secondary background
            bubble = QFrame()
            bubble_layout = QVBoxLayout()
            bubble_layout.setContentsMargins(Spacing.MD, Spacing.SM, Spacing.MD, Spacing.SM)
            bubble_layout.addWidget(msg_label)
            bubble.setLayout(bubble_layout)
            
            bubble.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_SECONDARY};
                    border: 1px solid {Colors.BORDER_LIGHT};
                    border-radius: {BorderRadius.MD}px;
                }}
            """)
            
            msg_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            
            container.addWidget(bubble)
            container.addStretch()
        
        layout.addLayout(container)
        self.setLayout(layout)
        self.setStyleSheet("background-color: transparent; border: none;")


class AIFinancialAdvisor(QWidget):
    """AI Financial Advisor - Chat interface for financial guidance"""
    
    def __init__(self, db: EnhancedDatabase, user_data: dict, user_type: str = "parent", parent=None):
        super().__init__(parent)
        self.db = db
        self.user_data = user_data
        self.user_type = user_type  # "parent" or "child"
        self.user_id = user_data['id']
        
        # Mock AI responses (would integrate OpenAI in production)
        self.ai_enabled = False
        self.init_ui()
        self.load_conversation_history()
    
    def init_ui(self):
        """Initialize advisor UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.LG)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(Spacing.SM)
        
        title = QLabel("💡 Financial Advisor")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        subtitle = QLabel("Get personalized financial advice and insights")
        subtitle.setFont(Fonts.body_sm())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Chat area
        chat_scroll = QScrollArea()
        chat_scroll.setWidgetResizable(True)
        chat_scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
            QScrollBar:vertical {{
                width: 8px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {Colors.BORDER_MEDIUM};
                border-radius: 4px;
            }}
        """)
        
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        self.chat_layout.setSpacing(Spacing.MD)
        
        self.chat_container.setLayout(self.chat_layout)
        chat_scroll.setWidget(self.chat_container)
        
        main_layout.addWidget(chat_scroll, 1)
        
        # Input area
        input_layout = QHBoxLayout()
        input_layout.setSpacing(Spacing.MD)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Ask about your finances, budgeting, spending habits...")
        self.message_input.setMinimumHeight(44)
        self.message_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
                padding: {Spacing.MD}px;
                font-size: 13px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.ACCENT};
            }}
        """)
        
        send_btn = QPushButton("Send")
        send_btn.setMinimumHeight(44)
        send_btn.setMinimumWidth(100)
        send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: {BorderRadius.MD}px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #2563eb;
            }}
            QPushButton:pressed {{
                background-color: #1e40af;
            }}
        """)
        send_btn.setCursor(Qt.PointingHandCursor)
        send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(send_btn)
        
        main_layout.addLayout(input_layout)
        
        self.setLayout(main_layout)
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        
        # Connect enter key
        self.message_input.returnPressed.connect(send_btn.click)
    
    def load_conversation_history(self):
        """Load previous conversation"""
        messages = self.db.get_ai_conversation(self.user_id, self.user_type)
        
        # Reverse to show oldest first
        for msg in reversed(messages):
            bubble = ChatBubble(
                msg['message_text'],
                is_user=msg['is_user_message']
            )
            self.chat_layout.addWidget(bubble)
        
        self.chat_layout.addStretch()
    
    def send_message(self):
        """Send message and get AI response"""
        user_message = self.message_input.text().strip()
        
        if not user_message:
            return
        
        # Clear input
        self.message_input.clear()
        
        # Add user message to chat
        user_bubble = ChatBubble(user_message, is_user=True)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, user_bubble)
        
        # Save to database
        self.db.add_ai_message(self.user_id, self.user_type, user_message, True)
        
        # Generate AI response
        ai_response = self.generate_ai_response(user_message)
        
        # Add AI response
        ai_bubble = ChatBubble(ai_response, is_user=False)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, ai_bubble)
        
        # Save to database
        self.db.add_ai_message(self.user_id, self.user_type, ai_response, False)
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def generate_ai_response(self, user_message: str) -> str:
        """Generate mock AI response (would call OpenAI API in production)"""
        
        # Mock responses based on keywords
        message_lower = user_message.lower()
        
        if "help" in message_lower or "how" in message_lower:
            return "I'm your financial advisor! I can help you with budgeting, spending analysis, saving strategies, and financial planning. What would you like to know?"
        
        elif "spending" in message_lower or "expense" in message_lower:
            return "Looking at your spending patterns, I notice opportunities to optimize your budget. Would you like me to analyze your expenses by category?"
        
        elif "save" in message_lower or "saving" in message_lower:
            return "Great focus on saving! I recommend the 50/30/20 rule: 50% needs, 30% wants, 20% savings. How does your current spending align with this?"
        
        elif "budget" in message_lower:
            return "Setting a budget is key to financial success. Let's review your income and expenses. I can help you create a personalized budget plan."
        
        elif "goal" in message_lower or "target" in message_lower:
            return "Setting financial goals is motivating! Whether it's saving for something special or building an emergency fund, I can help you track progress."
        
        elif "invest" in message_lower:
            return "Investment strategies vary based on age and goals. For long-term growth, consider diversification. Would you like to discuss investment options?"
        
        elif "child" in message_lower or "kid" in message_lower or "allowance" in message_lower:
            return "Teaching children financial literacy is important! Consider using the allowance system to teach budgeting and saving habits. How can I help?"
        
        else:
            return "That's a great question! To give you the best advice, could you provide more details about what you're trying to achieve financially?"
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        # This would be implemented with QScrollArea scrolling
        pass


class QuickInsights(QFrame):
    """Quick financial insights cards"""
    
    def __init__(self, title: str, value: str, insight: str, icon: str = "📊", 
                 color: str = Colors.SAVINGS, parent=None):
        super().__init__(parent)
        self.init_ui(title, value, insight, icon, color)
    
    def init_ui(self, title: str, value: str, insight: str, icon: str, color: str):
        """Initialize insights card"""
        layout = QVBoxLayout()
        layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        layout.setSpacing(Spacing.SM)
        
        # Icon and title
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 24))
        
        title_label = QLabel(title)
        title_label.setFont(Fonts.body_sm())
        title_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont(Fonts.FAMILY_PRIMARY, 20, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        # Insight
        insight_label = QLabel(insight)
        insight_label.setFont(Fonts.caption())
        insight_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        insight_label.setWordWrap(True)
        layout.addWidget(insight_label)
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {BorderRadius.MD}px;
            }}
        """)
