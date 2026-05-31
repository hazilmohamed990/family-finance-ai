from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

from database.queries import FinanceRepository
from models.expense_model import Expense


class DataService:
    def __init__(self, repo: FinanceRepository = None, user_id: int = 1):
        self.repo = repo or FinanceRepository()
        self.user_id = user_id
        self._seed_demo_data_if_empty()

    def _seed_demo_data_if_empty(self):
        if self.repo.get_income_total(self.user_id) > 0 or self.repo.get_expenses(self.user_id):
            return

        demo_income = [
            (4200.00, "Salary", "2024-02-15"),
            (1250.00, "Freelance", "2024-03-05"),
            (4200.00, "Salary", "2024-04-15"),
        ]
        demo_expenses = [
            ("Groceries", 312.25, "2024-02-02", "Weekly grocery run"),
            ("Utilities", 118.50, "2024-02-10", "Electric and water"),
            ("Transport", 64.80, "2024-02-11", "Monthly transit pass"),
            ("Dining", 89.20, "2024-02-18", "Family dinner out"),
            ("Entertainment", 45.00, "2024-02-23", "Movie night"),
            ("Groceries", 298.60, "2024-03-01", "Supermarket refill"),
            ("Healthcare", 52.00, "2024-03-08", "Pharmacy visit"),
            ("Savings", 100.00, "2024-03-12", "Emergency fund"),
            ("Utilities", 124.30, "2024-03-13", "Internet and gas"),
            ("Travel", 225.00, "2024-03-20", "Weekend trip"),
            ("Groceries", 324.10, "2024-04-02", "Grocery pickup"),
            ("Dining", 74.15, "2024-04-09", "Lunch with family"),
            ("Subscriptions", 33.99, "2024-04-11", "Streaming services"),
            ("Transport", 70.00, "2024-04-15", "Fuel and rideshare"),
        ]

        for amount, source, date in demo_income:
            self.repo.add_income(self.user_id, amount, source, date)
        for category, amount, date, description in demo_expenses:
            self.repo.add_expense(self.user_id, category, amount, date, description)

    def get_expenses(self, start_date: str = None, end_date: str = None, category: str = None) -> List[Expense]:
        rows = self.repo.get_expenses(self.user_id, start_date, end_date, category)
        return [Expense(id=row[0], user_id=self.user_id, category=row[1], amount=row[2], date=row[3], description=row[4] or "") for row in rows]

    def add_expense(self, category: str, amount: float, date: str, description: str = "") -> None:
        self.repo.add_expense(self.user_id, category, amount, date, description)

    def update_expense(self, expense_id: int, category: str, amount: float, date: str, description: str) -> None:
        self.repo.update_expense(expense_id, category, amount, date, description)

    def delete_expense(self, expense_id: int) -> None:
        self.repo.delete_expense(expense_id)

    def total_income(self) -> float:
        return self.repo.get_income_total(self.user_id)

    def total_expenses(self) -> float:
        return sum(expense.amount for expense in self.get_expenses())

    def summary(self) -> Dict[str, float]:
        income = self.total_income()
        expenses = self.total_expenses()
        savings = income - expenses
        return {
            "income": income,
            "expenses": expenses,
            "savings": savings,
            "balance": income - expenses,
        }

    def monthly_expense_trend(self) -> Tuple[List[str], List[float]]:
        expenses = self.get_expenses()
        totals = defaultdict(float)
        for expense in expenses:
            totals[expense.month_key()] += expense.amount

        sorted_months = sorted(totals.keys())
        return sorted_months, [totals[month] for month in sorted_months]

    def monthly_income_vs_expense(self) -> Tuple[List[str], List[float], List[float]]:
        months = set()
        expense_totals = defaultdict(float)
        for expense in self.get_expenses():
            month = expense.month_key()
            expense_totals[month] += expense.amount
            months.add(month)

        income_rows = self.repo.get_income_history(self.user_id)
        income_totals = defaultdict(float)
        for date_text, amount in income_rows:
            try:
                month = datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m")
            except ValueError:
                month = date_text
            income_totals[month] += amount
            months.add(month)

        sorted_months = sorted(months)
        income_values = [income_totals.get(month, 0.0) for month in sorted_months]
        expense_values = [expense_totals.get(month, 0.0) for month in sorted_months]
        return sorted_months, income_values, expense_values

    def category_distribution(self) -> Tuple[List[str], List[float]]:
        totals = defaultdict(float)
        for expense in self.get_expenses():
            totals[expense.category] += expense.amount

        categories = sorted(totals.keys(), key=lambda cat: totals[cat], reverse=True)
        amounts = [totals[cat] for cat in categories]
        return categories, amounts

    def savings_growth(self) -> Tuple[List[str], List[float]]:
        months = set()
        for date_text, amount in self.repo.get_income_history(self.user_id):
            try:
                month = datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m")
            except ValueError:
                month = date_text
            months.add(month)

        for expense in self.get_expenses():
            months.add(expense.month_key())

        months = sorted(months)
        balance_history = []
        cumulative = 0.0

        for month in months:
            income = 0.0
            for date_text, amount in self.repo.get_income_history(self.user_id):
                try:
                    income_month = datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m")
                except ValueError:
                    income_month = date_text
                if income_month == month:
                    income += amount
            expense = sum(exp.amount for exp in self.get_expenses() if exp.month_key() == month)
            cumulative += income - expense
            balance_history.append(cumulative)

        return months, balance_history

    def add_receipt(self, merchant: str, date: str, total: float, tax: float = None, payment_method: str = None, image_path: str = None, ocr_text: str = None):
        return self.repo.add_receipt(self.user_id, merchant, date, total, tax, payment_method, image_path, ocr_text)

    def get_receipts(self, limit: int = 100):
        return self.repo.get_receipts(self.user_id, limit)

