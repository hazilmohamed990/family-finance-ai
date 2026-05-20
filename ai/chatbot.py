import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class FinanceChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def respond(self, message, income=0, expenses=None):
        if expenses is None:
            expenses = []

        total_expenses = sum(e["amount"] for e in expenses)
        savings = income - total_expenses

        system_prompt = f"""
You are a smart financial assistant inside a family budgeting app.

User financial data:
- Income: {income}
- Expenses: {total_expenses}
- Savings: {savings}

Rules:
- Give short, clear advice
- Focus on saving money, budgeting, and spending habits
- Be practical and actionable
- Avoid long explanations
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.5
        )

        return response.choices[0].message.content
    
