import sqlite3


class Database:
    def __init__(self, db_name="finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_tables()

    def init_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT,
            amount REAL,
            date TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            source TEXT,
            date TEXT
        )
        """)

        self.conn.commit()

    def add_expense(self, user_id, category, amount, date):
        self.cursor.execute("""
        INSERT INTO expenses (user_id, category, amount, date)
        VALUES (?, ?, ?, ?)
        """, (user_id, category, amount, date))
        self.conn.commit()

    def add_income(self, user_id, amount, source, date):
        self.cursor.execute("""
        INSERT INTO income (user_id, amount, source, date)
        VALUES (?, ?, ?, ?)
        """, (user_id, amount, source, date))
        self.conn.commit()

    def get_expenses(self, user_id):
        self.cursor.execute("""
        SELECT category, amount FROM expenses WHERE user_id=?
        """, (user_id,))
        return self.cursor.fetchall()

    def get_income_total(self, user_id):
        self.cursor.execute("""
        SELECT SUM(amount) FROM income WHERE user_id=?
        """, (user_id,))
        result = self.cursor.fetchone()[0]
        return result if result else 0