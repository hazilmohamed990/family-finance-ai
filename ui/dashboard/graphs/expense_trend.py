from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from utils.chart_helpers import style_figure


class ExpenseTrendChart(QWidget):
    def __init__(self, data_service):
        super().__init__()
        self.data_service = data_service
        self.figure = Figure(figsize=(5, 3), facecolor="none")
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self._build_ui()
        self.update_chart()

    def _build_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 20px;
            }
        """)
        title = QLabel("Monthly Expense Trend")
        title.setStyleSheet("color: #B4DE8B; font-size: 16px; font-weight: 700;")
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_chart(self):
        self.ax.clear()
        months, totals = self.data_service.monthly_expense_trend()
        if months and any(totals):
            self.ax.plot(months, totals, marker="o", linewidth=2.5, color="#00C25A")
        else:
            self.ax.text(0.5, 0.5, "No expense data yet", ha="center", va="center", color="#E4F1D1", fontsize=12)

        self.ax.set_xlabel("Month")
        self.ax.set_ylabel("Expenses")
        self.ax.set_xticklabels(months, rotation=45, ha="right")
        style_figure(self.figure, self.ax)
        self.canvas.draw()
