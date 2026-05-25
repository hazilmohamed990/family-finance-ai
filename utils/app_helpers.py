"""
Application Utilities and Helper Functions
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class AppConfig:
    """Application configuration"""
    
    APP_NAME = "Family Finance AI"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Family Finance Team"
    
    # Database
    DB_NAME = "finance.db"
    
    # Paths
    ASSETS_DIR = "assets"
    ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
    IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
    DATA_DIR = "data"
    
    # Feature flags
    ENABLE_AI = True
    ENABLE_OCR = True
    ENABLE_CAMERA = False  # Requires camera device
    ENABLE_NOTIFICATIONS = True
    
    # Limits
    MAX_CHILDREN = 10
    MAX_BUDGET_CATEGORIES = 20
    MAX_GOALS_PER_CHILD = 10
    
    # Default values
    DEFAULT_MONTHLY_ALLOWANCE = 15.0
    DEFAULT_POINTS_FOR_GOAL = 50
    DEFAULT_POINTS_FOR_ACHIEVEMENT = 100


class FinancialHelper:
    """Financial calculation helpers"""
    
    @staticmethod
    def calculate_savings_rate(income: float, savings: float) -> float:
        """Calculate savings rate as percentage"""
        if income <= 0:
            return 0
        return (savings / income) * 100
    
    @staticmethod
    def calculate_expense_ratio(income: float, expenses: float) -> float:
        """Calculate expense ratio as percentage"""
        if income <= 0:
            return 0
        return (expenses / income) * 100
    
    @staticmethod
    def categorize_spending(amount: float) -> str:
        """Categorize spending level"""
        if amount < 10:
            return "Small"
        elif amount < 50:
            return "Medium"
        elif amount < 100:
            return "Large"
        else:
            return "Very Large"
    
    @staticmethod
    def calculate_goal_progress(current: float, target: float) -> int:
        """Calculate goal progress percentage"""
        if target <= 0:
            return 0
        return min(int((current / target) * 100), 100)
    
    @staticmethod
    def get_budget_status(spent: float, limit: float, threshold: float = 80) -> str:
        """Get budget status: OK, Warning, or Over"""
        if spent <= 0:
            return "OK"
        
        percentage = (spent / limit) * 100 if limit > 0 else 0
        
        if percentage >= 100:
            return "Over"
        elif percentage >= threshold:
            return "Warning"
        else:
            return "OK"
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount as currency string"""
        return f"${amount:,.2f}"
    
    @staticmethod
    def get_month_range(year: int, month: int) -> Tuple[str, str]:
        """Get first and last day of month"""
        from datetime import date, timedelta
        
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        return (first_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d"))


class PointsHelper:
    """Points and gamification helpers"""
    
    # Point values for different actions
    POINT_VALUES = {
        "first_transaction": 10,
        "spending_goal": 50,
        "daily_streak": 5,
        "weekly_goal": 50,
        "monthly_goal": 100,
        "achievement_unlock": 100,
        "savings_milestone": 100,
    }
    
    @staticmethod
    def calculate_level(total_points: int) -> int:
        """Calculate user level based on points"""
        return max(1, total_points // 250 + 1)
    
    @staticmethod
    def get_level_points(level: int) -> int:
        """Get total points needed for level"""
        return (level - 1) * 250
    
    @staticmethod
    def points_to_next_level(total_points: int) -> int:
        """Get points needed to reach next level"""
        current_level = PointsHelper.calculate_level(total_points)
        next_level_points = PointsHelper.get_level_points(current_level + 1)
        return max(0, next_level_points - total_points)
    
    @staticmethod
    def get_achievement_badges() -> Dict[str, Dict]:
        """Get all available achievement badges"""
        return {
            "first_step": {
                "name": "First Step",
                "description": "Make your first transaction",
                "icon": "👶",
            },
            "saver": {
                "name": "Saver",
                "description": "Save $50",
                "icon": "💎",
            },
            "goal_setter": {
                "name": "Goal Setter",
                "description": "Create your first savings goal",
                "icon": "🎯",
            },
            "consistent": {
                "name": "Consistent",
                "description": "Maintain a 30-day saving streak",
                "icon": "📈",
            },
            "wise_spender": {
                "name": "Wise Spender",
                "description": "Stay within budget for 3 months",
                "icon": "🧠",
            },
            "millionaire": {
                "name": "Millionaire",
                "description": "Save $1000",
                "icon": "💰",
            },
        }


class ValidationHelper:
    """Input validation helpers"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_amount(amount: str) -> Tuple[bool, Optional[float]]:
        """Validate currency amount"""
        try:
            value = float(amount)
            if value < 0:
                return False, None
            return True, value
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_child_name(name: str) -> bool:
        """Validate child name"""
        if not name or len(name) < 2 or len(name) > 50:
            return False
        return name.isalpha() or ' ' in name
    
    @staticmethod
    def validate_category(category: str, valid_categories: List[str]) -> bool:
        """Validate expense category"""
        return category in valid_categories


class PasswordHelper:
    """Password and authentication helpers"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password (simple implementation)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password"""
        return PasswordHelper.hash_password(password) == hashed
    
    @staticmethod
    def generate_session_token() -> str:
        """Generate session token"""
        import secrets
        return secrets.token_urlsafe(32)


class DateHelper:
    """Date and time helpers"""
    
    @staticmethod
    def get_today() -> str:
        """Get today's date as YYYY-MM-DD"""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_current_month() -> str:
        """Get current month as YYYY-MM"""
        return datetime.now().strftime("%Y-%m")
    
    @staticmethod
    def get_current_year() -> int:
        """Get current year"""
        return datetime.now().year
    
    @staticmethod
    def format_date(date_str: str, format_str: str = "%b %d, %Y") -> str:
        """Format date string"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime(format_str)
        except:
            return date_str
    
    @staticmethod
    def days_since(date_str: str) -> int:
        """Get days since given date"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            delta = datetime.now() - date_obj
            return delta.days
        except:
            return 0
    
    @staticmethod
    def is_today(date_str: str) -> bool:
        """Check if date is today"""
        return date_str == DateHelper.get_today()
    
    @staticmethod
    def is_this_month(date_str: str) -> bool:
        """Check if date is in current month"""
        return date_str.startswith(DateHelper.get_current_month())


class FileHelper:
    """File system helpers"""
    
    @staticmethod
    def ensure_directory(path: str) -> None:
        """Create directory if it doesn't exist"""
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def file_exists(path: str) -> bool:
        """Check if file exists"""
        return os.path.isfile(path)
    
    @staticmethod
    def save_json(data: Dict, filepath: str) -> bool:
        """Save data to JSON file"""
        try:
            FileHelper.ensure_directory(os.path.dirname(filepath))
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    @staticmethod
    def load_json(filepath: str) -> Optional[Dict]:
        """Load data from JSON file"""
        try:
            if FileHelper.file_exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
        return None


class NotificationHelper:
    """Notification helpers"""
    
    @staticmethod
    def get_budget_alert(category: str, spent: float, limit: float) -> Optional[str]:
        """Get budget alert message"""
        percentage = (spent / limit) * 100 if limit > 0 else 0
        
        if percentage >= 100:
            return f"⚠️ Budget Exceeded! You've spent ${spent:.2f} of ${limit:.2f} on {category}"
        elif percentage >= 80:
            return f"⚠️ Budget Warning! You've spent {percentage:.0f}% of your {category} budget"
        else:
            return None
    
    @staticmethod
    def get_savings_congratulation(amount: float, goal: str = "") -> str:
        """Get congratulation message for saving"""
        if goal:
            return f"🎉 Great job! You saved ${amount:.2f} toward {goal}!"
        else:
            return f"🎉 Excellent savings! You've saved ${amount:.2f}!"
    
    @staticmethod
    def get_spending_tip(amount: float) -> Optional[str]:
        """Get spending tip"""
        if amount < 10:
            return "💡 Small purchase - don't forget to track it!"
        elif amount < 50:
            return "💡 Moderate spending - stay on budget!"
        else:
            return "💡 Large purchase - make sure it's a planned expense!"
