"""
Premium Dashboard Page with analytics and charts
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from .theme import Colors, Fonts, Spacing
from .components import Card, StatCard, MetricCard, HSection, VSection


class DashboardPage(QWidget):
    """Premium analytics dashboard"""
    
    def __init__(self, data_service, parent=None):
        super().__init__(parent)
        self.data_service = data_service
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize dashboard UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(Spacing.XXL, Spacing.XXL, Spacing.XXL, Spacing.XXL)
        main_layout.setSpacing(Spacing.XXL)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(Spacing.SM)
        
        title = QLabel("Dashboard")
        title.setFont(Fonts.heading_2())
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        subtitle = QLabel("Financial Overview & Analytics")
        subtitle.setFont(Fonts.body_base())
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Scroll area for dashboard
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
        
        # Top stat cards
        stats_layout = QGridLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(Spacing.LG)
        
        self.income_card = StatCard("Total Income", "$0.00", "YTD")
        self.expense_card = StatCard("Total Expenses", "$0.00", "YTD")
        self.savings_card = StatCard("Net Savings", "$0.00", "YTD")
        self.rate_card = StatCard("Savings Rate", "0%", "Of Income")
        
        self.income_card.set_accent_color(Colors.INCOME)
        self.expense_card.set_accent_color(Colors.EXPENSE)
        self.savings_card.set_accent_color(Colors.SAVINGS)
        self.rate_card.set_accent_color(Colors.NEUTRAL)
        
        stats_layout.addWidget(self.income_card, 0, 0)
        stats_layout.addWidget(self.expense_card, 0, 1)
        stats_layout.addWidget(self.savings_card, 0, 2)
        stats_layout.addWidget(self.rate_card, 0, 3)
        
        scroll_layout.addLayout(stats_layout)
        
        # Charts section
        charts_section = VSection("Analytics")
        charts_container = QHBoxLayout()
        charts_container.setContentsMargins(0, 0, 0, 0)
        charts_container.setSpacing(Spacing.LG)
        
        # Cash flow chart
        self.cashflow_chart_container = Card()
        cashflow_layout = QVBoxLayout()
        cashflow_layout.setContentsMargins(0, 0, 0, 0)
        
        cashflow_title = QLabel("Cash Flow Trend")
        cashflow_title.setFont(Fonts.heading_5())
        cashflow_layout.addWidget(cashflow_title)
        
        self.cashflow_canvas = FigureCanvas(Figure(figsize=(6, 3), dpi=100))
        self.cashflow_canvas.setStyleSheet(f"background-color: {Colors.BG_SECONDARY};")
        cashflow_layout.addWidget(self.cashflow_canvas)
        
        self.cashflow_chart_container.layout.addLayout(cashflow_layout)
        charts_container.addWidget(self.cashflow_chart_container, 1)
        
        # Expense breakdown
        self.expense_chart_container = Card()
        expense_layout = QVBoxLayout()
        expense_layout.setContentsMargins(0, 0, 0, 0)
        
        expense_title = QLabel("Expense Breakdown")
        expense_title.setFont(Fonts.heading_5())
        expense_layout.addWidget(expense_title)
        
        self.expense_canvas = FigureCanvas(Figure(figsize=(4, 3), dpi=100))
        self.expense_canvas.setStyleSheet(f"background-color: {Colors.BG_SECONDARY};")
        expense_layout.addWidget(self.expense_canvas)
        
        self.expense_chart_container.layout.addLayout(expense_layout)
        charts_container.addWidget(self.expense_chart_container, 0)
        
        charts_section.content_layout.addLayout(charts_container)
        scroll_layout.addWidget(charts_section)
        
        # Insights section
        insights_section = VSection("Recent Insights")
        self.insights_layout = QVBoxLayout()
        self.insights_layout.setContentsMargins(0, 0, 0, 0)
        self.insights_layout.setSpacing(Spacing.MD)
        insights_section.content_layout.addLayout(self.insights_layout)
        scroll_layout.addWidget(insights_section)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def load_data(self):
        """Load financial data"""
        try:
            income, expenses = self.data_service.repo.get_financial_data(1)
            
            total_expenses = sum(e.get("amount", 0) for e in expenses)
            savings = income - total_expenses
            savings_rate = (savings / income * 100) if income > 0 else 0
            
            self.income_card.set_value(f"${income:,.2f}")
            self.expense_card.set_value(f"${total_expenses:,.2f}")
            self.savings_card.set_value(f"${savings:,.2f}")
            self.rate_card.set_value(f"{savings_rate:.1f}%")
            
            self._plot_cashflow(income, total_expenses)
            self._plot_expenses(expenses)
            self._load_insights()
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
    
    def _plot_cashflow(self, income: float, expenses: float):
        """Plot cash flow chart"""
        try:
            fig = self.cashflow_canvas.figure
            fig.clear()
            ax = fig.add_subplot(111)
            
            # Style
            ax.set_facecolor(Colors.BG_SECONDARY)
            fig.patch.set_facecolor(Colors.BG_SECONDARY)
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            income_data = [income * 0.8, income * 0.9, income, income * 1.1, income * 0.95, income]
            expense_data = [expenses * 1.1, expenses * 0.8, expenses, expenses * 0.9, expenses * 1.2, expenses]
            
            x = range(len(months))
            width = 0.35
            
            ax.bar([i - width/2 for i in x], income_data, width, label='Income', color=Colors.INCOME, alpha=0.8)
            ax.bar([i + width/2 for i in x], expense_data, width, label='Expenses', color=Colors.EXPENSE, alpha=0.8)
            
            ax.set_xlabel('Month', color=Colors.TEXT_SECONDARY, fontsize=11)
            ax.set_ylabel('Amount ($)', color=Colors.TEXT_SECONDARY, fontsize=11)
            ax.set_xticks(x)
            ax.set_xticklabels(months, color=Colors.TEXT_SECONDARY, fontsize=10)
            ax.tick_params(colors=Colors.TEXT_SECONDARY)
            ax.legend(loc='upper left', frameon=False, labelcolor=Colors.TEXT_SECONDARY)
            
            # Grid
            ax.grid(axis='y', alpha=0.2, color=Colors.BORDER_LIGHT, linestyle='-', linewidth=0.5)
            ax.set_axisbelow(True)
            
            # Spines
            for spine in ax.spines.values():
                spine.set_color(Colors.BORDER_LIGHT)
                spine.set_linewidth(0.5)
            
            fig.tight_layout()
            self.cashflow_canvas.draw()
        except Exception as e:
            print(f"Error plotting cashflow: {e}")
    
    def _plot_expenses(self, expenses: list):
        """Plot expense breakdown pie chart"""
        try:
            fig = self.expense_canvas.figure
            fig.clear()
            ax = fig.add_subplot(111)
            
            # Style
            ax.set_facecolor(Colors.BG_SECONDARY)
            fig.patch.set_facecolor(Colors.BG_SECONDARY)
            
            # Aggregate by category
            categories = {}
            for expense in expenses:
                category = expense.get('category', 'Other')
                amount = expense.get('amount', 0)
                categories[category] = categories.get(category, 0) + amount
            
            if not categories:
                categories = {'No Data': 1}
            
            labels = list(categories.keys())
            sizes = list(categories.values())
            colors = [Colors.CHART_1, Colors.CHART_2, Colors.CHART_3, Colors.CHART_4, Colors.CHART_5, Colors.CHART_6]
            
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)])
            
            for text in texts:
                text.set_color(Colors.TEXT_SECONDARY)
                text.set_fontsize(10)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(9)
                autotext.set_weight('bold')
            
            fig.tight_layout()
            self.expense_canvas.draw()
        except Exception as e:
            print(f"Error plotting expenses: {e}")
    
    def _load_insights(self):
        """Load and display financial insights"""
        try:
            from ai.analyzer import FinanceAnalyzer
            income, expenses = self.data_service.repo.get_financial_data(1)
            analyzer = FinanceAnalyzer(income, expenses)
            
            # Clear previous insights
            while self.insights_layout.count():
                self.insights_layout.takeAt(0).widget().deleteLater()
            
            for insight in analyzer.insights():
                insight_card = MetricCard("Insight", insight, color=Colors.INFO)
                self.insights_layout.addWidget(insight_card)
        except Exception as e:
            print(f"Error loading insights: {e}")
    
    def refresh(self):
        """Refresh dashboard data"""
        self.load_data()
