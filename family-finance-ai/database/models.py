class Expense:
    def __init__(self, category, amount, date):
        self.category = category
        self.amount = amount
        self.date = date


class Income:
    def __init__(self, amount, source, date):
        self.amount = amount
        self.source = source
        self.date = date