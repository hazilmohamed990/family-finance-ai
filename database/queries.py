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

    def add_receipt(self, user_id, merchant, date, total, tax=None, payment_method=None, image_path=None, ocr_text=None):
        return self.db.add_receipt(user_id, merchant, date, total, tax, payment_method, image_path, ocr_text)

    def get_receipts(self, user_id, limit=100):
        return self.db.get_receipts(user_id, limit)

    def get_receipt_by_id(self, receipt_id):
        return self.db.get_receipt_by_id(receipt_id)

    def add_ocr_history(self, receipt_id, ocr_text):
        return self.db.add_ocr_history(receipt_id, ocr_text)

    def add_ai_analysis(self, receipt_id, analysis_text, score=None, metadata=None):
        return self.db.add_ai_analysis(receipt_id, analysis_text, score, metadata)

    def get_ai_analysis(self, receipt_id):
        return self.db.get_ai_analysis(receipt_id)

