from dataclasses import dataclass
from datetime import datetime


@dataclass
class Expense:
    id: int
    user_id: int
    category: str
    amount: float
    date: str
    description: str = ""

    def month_key(self) -> str:
        try:
            return datetime.strptime(self.date, "%Y-%m-%d").strftime("%Y-%m")
        except ValueError:
            return self.date
