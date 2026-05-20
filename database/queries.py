from database.db import Database


class FinanceRepository:
    def __init__(self):
        self.db = Database()

    def add_expense(self, user_id, category, amount, date, description=""):
        self.db.add_expense(user_id, category, amount, date, description)

    def update_expense(self, expense_id, category, amount, date, description):
        self.db.update_expense(expense_id, category, amount, date, description)

    def delete_expense(self, expense_id):
        self.db.delete_expense(expense_id)

    def get_expenses(self, user_id, start_date=None, end_date=None, category=None):
        return self.db.get_expenses(user_id, start_date, end_date, category)

    def get_expense_by_id(self, expense_id):
        return self.db.get_expense_by_id(expense_id)

    def add_income(self, user_id, amount, source, date):
        self.db.add_income(user_id, amount, source, date)

    def get_income_total(self, user_id):
        return self.db.get_income_total(user_id)

    def get_income_history(self, user_id):
        return self.db.get_income_history(user_id)

    def get_financial_data(self, user_id):
        expenses = self.db.get_expenses(user_id)
        income = self.db.get_income_total(user_id)
        return income, [{"category": row[1], "amount": row[2], "date": row[3], "description": row[4]} for row in expenses]
