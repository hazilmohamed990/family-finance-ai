"""
Enhanced SQLite Database for Family Finance AI
Complete schema for dual interface, gamification, AI, and grocery scanning
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any


class EnhancedDatabase:
    """Complete database system with all features"""
    
    def __init__(self, db_name: str = "finance.db"):
        self.db_path = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_schema()
    
    def _init_schema(self):
        """Initialize complete database schema"""
        # Parent/User accounts
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS parents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Child accounts
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                avatar_color TEXT DEFAULT '#3B82F6',
                monthly_allowance REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES parents(id)
            )
        """)
        
        # Parent expenses (grocery, bills, etc)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS parent_expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                receipt_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES parents(id),
                FOREIGN KEY (receipt_id) REFERENCES receipts(id)
            )
        """)
        
        # Parent income
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS parent_income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER NOT NULL,
                source TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                recurring BOOLEAN DEFAULT 0,
                frequency TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES parents(id)
            )
        """)
        
        # Allowances - payments to children
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS allowances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                parent_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                frequency TEXT,
                status TEXT DEFAULT 'paid',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id),
                FOREIGN KEY (parent_id) REFERENCES parents(id)
            )
        """)
        
        # Child spending
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS child_spending (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                approved_by_parent BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        """)
        
        # Child savings/balance
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS child_savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL UNIQUE,
                current_balance REAL DEFAULT 0,
                total_saved REAL DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        """)
        
        # Points system
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                reason TEXT,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        """)
        
        # Achievements/Badges
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                badge_type TEXT NOT NULL,
                badge_name TEXT NOT NULL,
                description TEXT,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        """)
        
        # Savings goals
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                icon TEXT,
                color TEXT,
                deadline TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        """)
        
        # Receipts
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER NOT NULL,
                merchant TEXT NOT NULL,
                amount REAL NOT NULL,
                tax REAL DEFAULT 0,
                date TEXT NOT NULL,
                payment_method TEXT,
                image_path TEXT,
                ocr_text TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES parents(id)
            )
        """)
        
        # Food photos (kids upload photos of food)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                ai_analysis TEXT,
                expense_value REAL,
                healthiness_score INTEGER,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        """)
        
        # AI Chat history
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_type TEXT NOT NULL,
                message_text TEXT NOT NULL,
                is_user_message BOOLEAN NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Budgets
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                limit_amount REAL NOT NULL,
                alert_threshold REAL DEFAULT 80,
                month_year TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES parents(id)
            )
        """)
        
        # Notifications
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT,
                read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    # ========== PARENT METHODS ==========
    
    def add_parent(self, email: str, name: str, password_hash: str) -> int:
        """Add new parent account"""
        self.cursor.execute(
            "INSERT INTO parents (email, name, password_hash) VALUES (?, ?, ?)",
            (email, name, password_hash)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_parent(self, parent_id: int) -> Optional[Dict]:
        """Get parent by ID"""
        self.cursor.execute("SELECT * FROM parents WHERE id = ?", (parent_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_parent_by_email(self, email: str) -> Optional[Dict]:
        """Get parent by email"""
        self.cursor.execute("SELECT * FROM parents WHERE email = ?", (email,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    # ========== CHILD METHODS ==========
    
    def add_child(self, parent_id: int, name: str, age: int = None, 
                  monthly_allowance: float = 0) -> int:
        """Add new child"""
        self.cursor.execute(
            "INSERT INTO children (parent_id, name, age, monthly_allowance) VALUES (?, ?, ?, ?)",
            (parent_id, name, age, monthly_allowance)
        )
        self.conn.commit()
        child_id = self.cursor.lastrowid
        
        # Initialize child savings
        self.cursor.execute(
            "INSERT INTO child_savings (child_id) VALUES (?)",
            (child_id,)
        )
        self.conn.commit()
        
        return child_id
    
    def get_children(self, parent_id: int) -> List[Dict]:
        """Get all children for a parent"""
        self.cursor.execute(
            "SELECT * FROM children WHERE parent_id = ? ORDER BY name",
            (parent_id,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_child(self, child_id: int) -> Optional[Dict]:
        """Get child by ID"""
        self.cursor.execute("SELECT * FROM children WHERE id = ?", (child_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    # ========== EXPENSE METHODS ==========
    
    def add_parent_expense(self, parent_id: int, category: str, amount: float, 
                           description: str = "", date: str = None, 
                           receipt_id: int = None) -> int:
        """Add parent expense"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO parent_expenses (parent_id, category, amount, description, date, receipt_id) VALUES (?, ?, ?, ?, ?, ?)",
            (parent_id, category, amount, description, date, receipt_id)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_parent_expenses(self, parent_id: int, start_date: str = None, 
                           end_date: str = None, category: str = None) -> List[Dict]:
        """Get parent expenses with optional filters"""
        query = "SELECT * FROM parent_expenses WHERE parent_id = ?"
        params = [parent_id]
        
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
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def update_parent_expense(self, expense_id: int, category: str = None, 
                             amount: float = None, description: str = None, 
                             date: str = None) -> None:
        """Update parent expense"""
        updates = []
        params = []
        
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if amount is not None:
            updates.append("amount = ?")
            params.append(amount)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if date is not None:
            updates.append("date = ?")
            params.append(date)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE parent_expenses SET {', '.join(updates)} WHERE id = ?"
            params.append(expense_id)
            self.cursor.execute(query, params)
            self.conn.commit()
    
    def delete_parent_expense(self, expense_id: int) -> None:
        """Delete parent expense"""
        self.cursor.execute("DELETE FROM parent_expenses WHERE id = ?", (expense_id,))
        self.conn.commit()
    
    # ========== INCOME METHODS ==========
    
    def add_parent_income(self, parent_id: int, source: str, amount: float, 
                         date: str = None, recurring: bool = False, 
                         frequency: str = None) -> int:
        """Add parent income"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO parent_income (parent_id, source, amount, date, recurring, frequency) VALUES (?, ?, ?, ?, ?, ?)",
            (parent_id, source, amount, date, recurring, frequency)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_parent_income(self, parent_id: int, start_date: str = None, 
                         end_date: str = None) -> List[Dict]:
        """Get parent income"""
        query = "SELECT * FROM parent_income WHERE parent_id = ?"
        params = [parent_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date DESC"
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_total_parent_income(self, parent_id: int, start_date: str = None, 
                               end_date: str = None) -> float:
        """Get total parent income"""
        query = "SELECT SUM(amount) as total FROM parent_income WHERE parent_id = ?"
        params = [parent_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        return result['total'] or 0 if result else 0
    
    # ========== ALLOWANCE METHODS ==========
    
    def add_allowance(self, child_id: int, parent_id: int, amount: float, 
                     date: str = None, frequency: str = "monthly") -> int:
        """Add allowance payment"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO allowances (child_id, parent_id, amount, date, frequency) VALUES (?, ?, ?, ?, ?)",
            (child_id, parent_id, amount, date, frequency)
        )
        self.conn.commit()
        
        # Add to child's savings
        self.add_to_child_savings(child_id, amount)
        
        return self.cursor.lastrowid
    
    def get_child_allowances(self, child_id: int) -> List[Dict]:
        """Get all allowances for a child"""
        self.cursor.execute(
            "SELECT * FROM allowances WHERE child_id = ? ORDER BY date DESC",
            (child_id,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== CHILD SPENDING METHODS ==========
    
    def add_child_spending(self, child_id: int, category: str, amount: float, 
                          description: str = "", date: str = None, 
                          approved: bool = True) -> int:
        """Add child spending"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO child_spending (child_id, category, amount, description, date, approved_by_parent) VALUES (?, ?, ?, ?, ?, ?)",
            (child_id, category, amount, description, date, approved)
        )
        self.conn.commit()
        
        # Deduct from savings
        if approved:
            self.deduct_from_child_savings(child_id, amount)
        
        return self.cursor.lastrowid
    
    def get_child_spending(self, child_id: int, start_date: str = None, 
                          end_date: str = None) -> List[Dict]:
        """Get child spending"""
        query = "SELECT * FROM child_spending WHERE child_id = ?"
        params = [child_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date DESC"
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== CHILD SAVINGS METHODS ==========
    
    def add_to_child_savings(self, child_id: int, amount: float) -> None:
        """Add to child's savings"""
        self.cursor.execute(
            "UPDATE child_savings SET current_balance = current_balance + ?, total_saved = total_saved + ?, last_updated = CURRENT_TIMESTAMP WHERE child_id = ?",
            (amount, amount, child_id)
        )
        self.conn.commit()
    
    def deduct_from_child_savings(self, child_id: int, amount: float) -> None:
        """Deduct from child's savings"""
        self.cursor.execute(
            "UPDATE child_savings SET current_balance = current_balance - ?, last_updated = CURRENT_TIMESTAMP WHERE child_id = ?",
            (amount, child_id)
        )
        self.conn.commit()
    
    def get_child_savings(self, child_id: int) -> Optional[Dict]:
        """Get child's savings info"""
        self.cursor.execute("SELECT * FROM child_savings WHERE child_id = ?", (child_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    # ========== POINTS METHODS ==========
    
    def add_points(self, child_id: int, amount: int, reason: str = "") -> int:
        """Add points to child"""
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            "INSERT INTO points (child_id, amount, reason, date) VALUES (?, ?, ?, ?)",
            (child_id, amount, reason, date)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_total_points(self, child_id: int) -> int:
        """Get total points for child"""
        self.cursor.execute("SELECT SUM(amount) as total FROM points WHERE child_id = ?", (child_id,))
        result = self.cursor.fetchone()
        return result['total'] or 0 if result else 0
    
    def get_points_history(self, child_id: int) -> List[Dict]:
        """Get points history"""
        self.cursor.execute(
            "SELECT * FROM points WHERE child_id = ? ORDER BY date DESC",
            (child_id,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== ACHIEVEMENT METHODS ==========
    
    def add_achievement(self, child_id: int, badge_type: str, badge_name: str, 
                       description: str = "") -> int:
        """Add achievement badge"""
        self.cursor.execute(
            "INSERT INTO achievements (child_id, badge_type, badge_name, description) VALUES (?, ?, ?, ?)",
            (child_id, badge_type, badge_name, description)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_achievements(self, child_id: int) -> List[Dict]:
        """Get achievements for child"""
        self.cursor.execute(
            "SELECT * FROM achievements WHERE child_id = ? ORDER BY unlocked_at DESC",
            (child_id,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== SAVINGS GOALS METHODS ==========
    
    def add_savings_goal(self, child_id: int, goal_name: str, target_amount: float, 
                        icon: str = "🎯", color: str = "#3B82F6", 
                        deadline: str = None) -> int:
        """Add savings goal"""
        self.cursor.execute(
            "INSERT INTO savings_goals (child_id, goal_name, target_amount, icon, color, deadline) VALUES (?, ?, ?, ?, ?, ?)",
            (child_id, goal_name, target_amount, icon, color, deadline)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_savings_goals(self, child_id: int, include_completed: bool = False) -> List[Dict]:
        """Get savings goals"""
        if include_completed:
            query = "SELECT * FROM savings_goals WHERE child_id = ? ORDER BY created_at DESC"
        else:
            query = "SELECT * FROM savings_goals WHERE child_id = ? AND completed = 0 ORDER BY created_at DESC"
        
        self.cursor.execute(query, (child_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def update_goal_progress(self, goal_id: int, current_amount: float) -> None:
        """Update goal progress"""
        self.cursor.execute(
            "SELECT target_amount FROM savings_goals WHERE id = ?",
            (goal_id,)
        )
        goal = self.cursor.fetchone()
        
        if goal and current_amount >= goal['target_amount']:
            completed = 1
        else:
            completed = 0
        
        self.cursor.execute(
            "UPDATE savings_goals SET current_amount = ?, completed = ? WHERE id = ?",
            (current_amount, completed, goal_id)
        )
        self.conn.commit()
    
    # ========== RECEIPT METHODS ==========
    
    def add_receipt(self, parent_id: int, merchant: str, amount: float, 
                   date: str = None, tax: float = 0, payment_method: str = None, 
                   image_path: str = None, ocr_text: str = None, 
                   category: str = None) -> int:
        """Add receipt"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO receipts (parent_id, merchant, amount, tax, date, payment_method, image_path, ocr_text, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (parent_id, merchant, amount, tax, date, payment_method, image_path, ocr_text, category)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_receipts(self, parent_id: int) -> List[Dict]:
        """Get receipts"""
        self.cursor.execute(
            "SELECT * FROM receipts WHERE parent_id = ? ORDER BY date DESC",
            (parent_id,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== FOOD PHOTO METHODS ==========
    
    def add_food_photo(self, child_id: int, image_path: str, date: str = None, 
                      ai_analysis: str = None, expense_value: float = None, 
                      healthiness_score: int = None) -> int:
        """Add food photo"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO food_photos (child_id, image_path, date, ai_analysis, expense_value, healthiness_score) VALUES (?, ?, ?, ?, ?, ?)",
            (child_id, image_path, date, ai_analysis, expense_value, healthiness_score)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_food_photos(self, child_id: int) -> List[Dict]:
        """Get food photos"""
        self.cursor.execute(
            "SELECT * FROM food_photos WHERE child_id = ? ORDER BY date DESC",
            (child_id,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== AI CONVERSATION METHODS ==========
    
    def add_ai_message(self, user_id: int, user_type: str, message: str, 
                      is_user_message: bool) -> int:
        """Add AI conversation message"""
        self.cursor.execute(
            "INSERT INTO ai_conversations (user_id, user_type, message_text, is_user_message) VALUES (?, ?, ?, ?)",
            (user_id, user_type, message, is_user_message)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_ai_conversation(self, user_id: int, user_type: str, limit: int = 50) -> List[Dict]:
        """Get AI conversation history"""
        self.cursor.execute(
            "SELECT * FROM ai_conversations WHERE user_id = ? AND user_type = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, user_type, limit)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== BUDGET METHODS ==========
    
    def add_budget(self, parent_id: int, category: str, limit_amount: float, 
                  month_year: str = None, alert_threshold: float = 80) -> int:
        """Add budget"""
        if month_year is None:
            month_year = datetime.now().strftime("%Y-%m")
        
        self.cursor.execute(
            "INSERT INTO budgets (parent_id, category, limit_amount, alert_threshold, month_year) VALUES (?, ?, ?, ?, ?)",
            (parent_id, category, limit_amount, alert_threshold, month_year)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_budgets(self, parent_id: int, month_year: str = None) -> List[Dict]:
        """Get budgets"""
        if month_year is None:
            month_year = datetime.now().strftime("%Y-%m")
        
        self.cursor.execute(
            "SELECT * FROM budgets WHERE parent_id = ? AND month_year = ?",
            (parent_id, month_year)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== NOTIFICATION METHODS ==========
    
    def add_notification(self, user_id: int, user_type: str, title: str, 
                        message: str, notification_type: str = "info") -> int:
        """Add notification"""
        self.cursor.execute(
            "INSERT INTO notifications (user_id, user_type, title, message, notification_type) VALUES (?, ?, ?, ?, ?)",
            (user_id, user_type, title, message, notification_type)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_notifications(self, user_id: int, user_type: str, unread_only: bool = False) -> List[Dict]:
        """Get notifications"""
        if unread_only:
            query = "SELECT * FROM notifications WHERE user_id = ? AND user_type = ? AND read = 0 ORDER BY created_at DESC"
        else:
            query = "SELECT * FROM notifications WHERE user_id = ? AND user_type = ? ORDER BY created_at DESC"
        
        self.cursor.execute(query, (user_id, user_type))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def mark_notification_read(self, notification_id: int) -> None:
        """Mark notification as read"""
        self.cursor.execute("UPDATE notifications SET read = 1 WHERE id = ?", (notification_id,))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        self.conn.close()
