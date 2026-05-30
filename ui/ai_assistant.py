"""
Modern AI Chat Interface with message bubbles
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton,
    QScrollArea, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import pyqtSignal

from .theme import Colors, Fonts, Spacing, BorderRadius
from .components import Card, PrimaryButton, PremiumLineEdit, VSection


class MessageBubble(QFrame):
    """Message bubble for chat"""
    
    def __init__(self, message: str, is_user: bool = True, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.MD)
        
        # Spacer for alignment
        if is_user:
            layout.addStretch()
        
        # Message bubble
        bubble = QFrame()
        bubble_layout = QVBoxLayout()
        bubble_layout.setContentsMargins(Spacing.MD, Spacing.SM, Spacing.MD, Spacing.SM)
        
        msg_label = QLabel(message)
        msg_label.setFont(Fonts.body_base())
        msg_label.setWordWrap(True)
        
        if is_user:
            bubble.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.ACCENT};
                    border-radius: {BorderRadius.MD}px;
                }}
            """)
            msg_label.setStyleSheet(f"color: white;")
        else:
            bubble.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_TERTIARY};
                    border-radius: {BorderRadius.MD}px;
                }}
            """)
            msg_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        bubble_layout.addWidget(msg_label)
        bubble.setLayout(bubble_layout)
        bubble.setMaximumWidth(600)
        
        layout.addWidget(bubble)
        
        # Spacer for alignment
        if not is_user:
            layout.addStretch()
        
        self.setLayout(layout)
        self.setFrameShape(QFrame.NoFrame)


class ModernAIAssistantPage(QWidget):
    """Modern AI assistant with chat interface"""
    
    def __init__(self, repo, parent=None):
        super().__init__(parent)
        self.repo = repo
        self.chatbot = None
        
        try:
            from ai.chatbot import FinanceChatbot
            self.chatbot = FinanceChatbot()
        except Exception:
            pass
        
        self.init_ui()
        self.load_summary()
    
    def init_ui(self):
        """Initialize AI assistant UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(Spacing.SM)
        
        title = QLabel("AI Financial Assistant")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        subtitle = QLabel("Ask questions about your finances or get personalized recommendations")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Chat container
        chat_container = Card()
        chat_container.layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area for chat
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Colors.BG_SECONDARY};
                border: none;
                border-radius: {BorderRadius.LG}px;
            }}
        """)
        
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        self.chat_layout.setSpacing(Spacing.MD)
        self.chat_widget.setLayout(self.chat_layout)
        
        scroll.setWidget(self.chat_widget)
        chat_container.layout.addWidget(scroll, 1)
        
        # Input area
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(Spacing.MD)
        
        self.input_field = PremiumLineEdit("Ask about budgeting, spending, or get AI insights...")
        self.input_field.returnPressed.connect(self.send_message)
        
        send_btn = PrimaryButton("Send")
        send_btn.setFixedWidth(80)
        send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        
        chat_container.layout.addLayout(input_layout)
        
        main_layout.addWidget(chat_container, 1)
        
        self.setLayout(main_layout)
    
    def load_summary(self):
        """Load and display initial summary"""
        try:
            from ai.analyzer import FinanceAnalyzer
            income, expenses = self.repo.get_financial_data(1)
            analyzer = FinanceAnalyzer(income, expenses)
            
            summary_msg = (
                f"Account Summary:\n"
                f"Income: ${income:,.2f}\n"
                f"Expenses: ${analyzer.total_expenses():,.2f}\n"
                f"Savings: ${analyzer.savings():,.2f}"
            )
            
            bubble = MessageBubble(summary_msg, is_user=False)
            self.chat_layout.addWidget(bubble)
            
            for insight in analyzer.insights():
                insight_bubble = MessageBubble(f"💡 {insight}", is_user=False)
                self.chat_layout.addWidget(insight_bubble)
            
            self.chat_layout.addStretch()
        except Exception as e:
            error_bubble = MessageBubble(f"Unable to load summary: {e}", is_user=False)
            self.chat_layout.addWidget(error_bubble)
    
    def send_message(self):
        """Send message to AI assistant"""
        message = self.input_field.text().strip()
        if not message:
            return
        
        # Add user message
        user_bubble = MessageBubble(message, is_user=True)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, user_bubble)
        self.input_field.clear()
        
        # Scroll to latest
        scroll = self.chat_layout.parent().parent()
        if scroll:
            scroll.verticalScrollBar().setValue(scroll.verticalScrollBar().maximum())
        
        if not self.chatbot:
            error_bubble = MessageBubble("AI assistant unavailable (OpenAI not configured).", is_user=False)
            self.chat_layout.insertWidget(self.chat_layout.count() - 1, error_bubble)
            return
        
        try:
            income, expenses = self.repo.get_financial_data(1)
            response = self.chatbot.respond(message, income=income, expenses=expenses)
            
            ai_bubble = MessageBubble(response, is_user=False)
            self.chat_layout.insertWidget(self.chat_layout.count() - 1, ai_bubble)
        except Exception as e:
            error_bubble = MessageBubble(f"Error: {str(e)}", is_user=False)
            self.chat_layout.insertWidget(self.chat_layout.count() - 1, error_bubble)
    
    def load_ai_summary(self):
        """Refresh summary (callback for other pages)"""
        self.load_summary()
