import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClientWrapper:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None

        if not self.api_key:
            print("❌ No GEMINI_API_KEY found")
            return

        try:
            self.client = genai.Client(api_key=self.api_key)
            print("✅ Gemini client initialized")
        except Exception as e:
            print("❌ Gemini init failed:", e)
            self.client = None

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.5):
        if not self.client:
            return self._fallback_response(system_prompt, user_message)

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{system_prompt}\n\nUser: {user_message}",
            )

            return response.text

        except Exception as e:
            print("❌ Gemini request failed:", e)
            return self._fallback_response(system_prompt, user_message)

    def _fallback_response(self, system_prompt: str, user_message: str):
        msg = user_message.lower()

        if "save" in msg or "saving" in msg:
            return "Try allocating a fixed % of income to savings each month."
        if "budget" in msg or "spend" in msg:
            return "Review top expense categories and set limits."
        if "receipt" in msg or "scan" in msg:
            return "Use receipt scanning to track purchases accurately."

        return "I can help analyze your finances—ask about spending or savings."


class FinanceChatbot:
    def __init__(self):
        self.client = GeminiClientWrapper()

    def respond(self, message, income=0, expenses=None):
        if expenses is None:
            expenses = []

        total_expenses = sum(e.get("amount", 0) for e in expenses)
        savings = income - total_expenses

        system_prompt = f"""
You are a concise financial assistant.
Income: {income}
Expenses: {total_expenses}
Savings: {savings}
Give short actionable advice.
"""

        return self.client.chat(system_prompt, message)