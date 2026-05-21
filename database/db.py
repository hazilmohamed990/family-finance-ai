import sqlite3


class Database:
    def __init__(self, db_name="finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_tables()
        self._create_extra_tables()

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
            date TEXT,
            description TEXT DEFAULT ''
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
        self._ensure_column("expenses", "description", "TEXT DEFAULT ''")

    def _ensure_column(self, table, column, column_definition):
        self.cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in self.cursor.fetchall()]
        if column not in columns:
            self.cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_definition}")
            self.conn.commit()

    def add_expense(self, user_id, category, amount, date, description=""):
        self.cursor.execute("""
        INSERT INTO expenses (user_id, category, amount, date, description)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, category, amount, date, description))
        self.conn.commit()

    def add_income(self, user_id, amount, source, date):
        self.cursor.execute("""
        INSERT INTO income (user_id, amount, source, date)
        VALUES (?, ?, ?, ?)
        """, (user_id, amount, source, date))
        self.conn.commit()

    def get_expenses(self, user_id, start_date=None, end_date=None, category=None):
        query = "SELECT id, category, amount, date, description FROM expenses WHERE user_id=?"
        params = [user_id]
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if category:
            query += " AND category = ?"
            params.append(category)
        query += " ORDER BY date DESC"
        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

    def get_expense_by_id(self, expense_id):
        self.cursor.execute(
            "SELECT id, user_id, category, amount, date, description FROM expenses WHERE id=?",
            (expense_id,)
        )
        return self.cursor.fetchone()

    def update_expense(self, expense_id, category, amount, date, description):
        self.cursor.execute(
            """
            UPDATE expenses
            SET category = ?, amount = ?, date = ?, description = ?
            WHERE id = ?
            """,
            (category, amount, date, description, expense_id)
        )
        self.conn.commit()

    def delete_expense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self.conn.commit()

    def get_income_history(self, user_id):
        self.cursor.execute(
            "SELECT date, amount FROM income WHERE user_id=? ORDER BY date",
            (user_id,)
        )
        return self.cursor.fetchall()

    def get_income_total(self, user_id):
        self.cursor.execute("""
        SELECT SUM(amount) FROM income WHERE user_id=?
        """, (user_id,))
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def _create_extra_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            merchant TEXT,
            date TEXT,
            total REAL,
            tax REAL,
            payment_method TEXT,
            image_path TEXT,
            ocr_text TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocr_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER,
            ocr_text TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER,
            analysis_text TEXT,
            score REAL,
            metadata TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """)
        self.conn.commit()

    def add_receipt(self, user_id, merchant, date, total, tax=None, payment_method=None, image_path=None, ocr_text=None):
        self.cursor.execute("""
        INSERT INTO receipts (user_id, merchant, date, total, tax, payment_method, image_path, ocr_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, merchant, date, total, tax, payment_method, image_path, ocr_text))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_receipts(self, user_id, limit=100):
        self.cursor.execute("""SELECT id, merchant, date, total, tax, payment_method, image_path, ocr_text FROM receipts WHERE user_id=? ORDER BY date DESC LIMIT ?""", (user_id, limit))
        return self.cursor.fetchall()

    def get_receipt_by_id(self, receipt_id):
        self.cursor.execute("""SELECT id, user_id, merchant, date, total, tax, payment_method, image_path, ocr_text FROM receipts WHERE id=?""", (receipt_id,))
        return self.cursor.fetchone()

    def add_ocr_history(self, receipt_id, ocr_text):
        self.cursor.execute("""
        INSERT INTO ocr_history (receipt_id, ocr_text)
        VALUES (?, ?)
        """, (receipt_id, ocr_text))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_ai_analysis(self, receipt_id, analysis_text, score=None, metadata=None):
        self.cursor.execute("""
        INSERT INTO ai_analysis (receipt_id, analysis_text, score, metadata)
        VALUES (?, ?, ?, ?)
        """, (receipt_id, analysis_text, score, metadata))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_ai_analysis(self, receipt_id):
        self.cursor.execute("""SELECT id, analysis_text, score, metadata, created_at FROM ai_analysis WHERE receipt_id=? ORDER BY created_at DESC""", (receipt_id,))
        return self.cursor.fetchall()
