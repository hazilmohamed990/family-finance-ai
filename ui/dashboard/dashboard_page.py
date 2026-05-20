from PyQt5.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt

from core.data_service import DataService
from ui.dashboard.graphs.category_pie import CategoryPieChart
from ui.dashboard.graphs.expense_trend import ExpenseTrendChart
from ui.dashboard.graphs.income_vs_expense import IncomeVsExpenseChart
from ui.dashboard.graphs.savings_trend import SavingsTrendChart


class DashboardPage(QWidget):
    def __init__(self, data_service=None):
        super().__init__()
        self.data_service = data_service or DataService()
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        self.summary_grid = QGridLayout()
        self.summary_grid.setSpacing(16)

        self.balance_card = self._create_summary_card("Account Balance", "$0.00")
        self.income_card = self._create_summary_card("Total Income", "$0.00")
        self.expenses_card = self._create_summary_card("Total Expenses", "$0.00")
        self.savings_card = self._create_summary_card("Net Savings", "$0.00")

        self.summary_grid.addWidget(self.balance_card, 0, 0)
        self.summary_grid.addWidget(self.income_card, 0, 1)
        self.summary_grid.addWidget(self.expenses_card, 0, 2)
        self.summary_grid.addWidget(self.savings_card, 0, 3)

        layout.addLayout(self.summary_grid)

        self.graph_grid = QGridLayout()
        self.graph_grid.setSpacing(20)

        self.expense_trend = ExpenseTrendChart(self.data_service)
        self.income_vs_expense = IncomeVsExpenseChart(self.data_service)
        self.category_pie = CategoryPieChart(self.data_service)
        self.savings_trend = SavingsTrendChart(self.data_service)

        self.graph_grid.addWidget(self.expense_trend, 0, 0)
        self.graph_grid.addWidget(self.income_vs_expense, 0, 1)
        self.graph_grid.addWidget(self.category_pie, 1, 0)
        self.graph_grid.addWidget(self.savings_trend, 1, 1)

        layout.addLayout(self.graph_grid)
        self.setLayout(layout)

    def _create_summary_card(self, title, value):
        card = QFrame()
        card.setObjectName("summaryCard")
        card.setStyleSheet("""
            QFrame#summaryCard {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 22px;
            }
        """)
        card.setMinimumHeight(130)
        inner_layout = QVBoxLayout()
        inner_layout.setContentsMargins(20, 16, 20, 16)
        inner_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #B4DE8B; font-size: 14px; font-weight: 600;")
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 28px; font-weight: 800;")
        value_label.setObjectName("valueLabel")

        inner_layout.addWidget(title_label)
        inner_layout.addStretch()
        inner_layout.addWidget(value_label)
        card.setLayout(inner_layout)
        return card

    def refresh(self):
        summary = self.data_service.summary()
        self._set_summary_value(self.balance_card, f"${summary['balance']:,.2f}")
        self._set_summary_value(self.income_card, f"${summary['income']:,.2f}")
        self._set_summary_value(self.expenses_card, f"${summary['expenses']:,.2f}")
        self._set_summary_value(self.savings_card, f"${summary['savings']:,.2f}")

        self.expense_trend.update_chart()
        self.income_vs_expense.update_chart()
        self.category_pie.update_chart()
        self.savings_trend.update_chart()

    def _set_summary_value(self, card, text):
        for child in card.findChildren(QLabel):
            if child.objectName() == "valueLabel":
                child.setText(text)
                return
