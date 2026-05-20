from datetime import datetime


class FinanceAnalyzer:
    def __init__(self, income, expenses):
        self.income = income
        self.expenses = expenses

    def total_expenses(self):
        return sum(e["amount"] for e in self.expenses)

    def savings(self):
        return self.income - self.total_expenses()

    def category_breakdown(self):
        b = {}
        for e in self.expenses:
            c = e["category"]
            b[c] = b.get(c, 0) + e["amount"]
        return b

    def insights(self):
        out = []

        if self.income == 0:
            return ["No income data"]

        savings = self.savings()
        total = self.total_expenses()

        if savings < 0:
            out.append("Overspending detected")
        elif savings < self.income * 0.1:
            out.append("Low savings warning")
        else:
            out.append("Healthy savings")

        if total > self.income * 0.8:
            out.append("High spending ratio")

        if self.expenses:
            top = max(self.category_breakdown(), key=self.category_breakdown().get)
            out.append(f"Top category: {top}")

        return out

    def summary(self):
        return {
            "income": self.income,
            "expenses": self.total_expenses(),
            "savings": self.savings(),
            "date": datetime.now().strftime("%Y-%m")
        }