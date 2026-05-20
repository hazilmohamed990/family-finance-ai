from database.db import Database


class FinanceRepository:
    def __init__(self):
        self.db = Database()

    def add_expense(self, user_id, category, amount, date):
        self.db.add_expense(user_id, category, amount, date)

    def add_income(self, user_id, amount, source, date):
        self.db.add_income(user_id, amount, source, date)

    def get_financial_data(self, user_id):
        expenses = self.db.get_expenses(user_id)
        income = self.db.get_income_total(user_id)

        return income, [{"category": c, "amount": a} for c, a in expenses]