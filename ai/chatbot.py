import os
from dotenv import load_dotenv

load_dotenv()


class GeminiClientWrapper:
    """A minimal wrapper that attempts to use Google's Gemini SDK if available.

    Falls back to a deterministic, safe local responder when the SDK or key
    is not available so the application never crashes.
    """

    def __init__(self):
        self.client = None
        self.api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        # Try to import the common Gemini SDK packages gracefully
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai
        except Exception:
            try:
                import googleai
                # hypothetical API
                googleai.configure(api_key=self.api_key)
                self.client = googleai
            except Exception:
                self.client = None

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.5):
        if not self.client or not self.api_key:
            # Fallback: simple heuristic responder
            return self._fallback_response(system_prompt, user_message)
        try:
            # Attempt to use a common pattern for generative APIs
            # This code is defensive: different SDKs expose different call shapes
            if hasattr(self.client, 'chat'):
                resp = self.client.chat.create(messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_message}
                ], temperature=temperature)
                # Normalize response
                if hasattr(resp, 'candidates') and resp.candidates:
                    return resp.candidates[0].content
                if hasattr(resp, 'choices') and resp.choices:
                    return getattr(resp.choices[0], 'message', getattr(resp.choices[0], 'content', ''))
                return str(resp)
            elif hasattr(self.client, 'generate'):
                resp = self.client.generate(prompt=system_prompt + "\n" + user_message, temperature=temperature)
                if hasattr(resp, 'text'):
                    return resp.text
                return str(resp)
            else:
                return self._fallback_response(system_prompt, user_message)
        except Exception:
            return self._fallback_response(system_prompt, user_message)

    def _fallback_response(self, system_prompt: str, user_message: str):
        # Lightweight deterministic assistant: extracts keywords and gives simple guidance
        msg = user_message.lower()
        if 'save' in msg or 'saving' in msg:
            return "Try allocating a fixed % of income to a savings goal each month."
        if 'budget' in msg or 'spend' in msg:
            return "Review your top 3 expense categories and set limits — groceries, subscriptions, transport."
        if 'receipt' in msg or 'scan' in msg:
            return "Use the receipt scanner to capture purchases; verify merchant and amount before saving."
        return "I can help analyze spending — try asking about your top expenses or how to save more."


class FinanceChatbot:
    def __init__(self):
        self.client = GeminiClientWrapper()

    def respond(self, message, income=0, expenses=None):
        if expenses is None:
            expenses = []

        total_expenses = sum(e.get('amount', 0) for e in expenses)
        savings = income - total_expenses

        system_prompt = f"""
You are a concise, practical financial assistant embedded in a family budgeting app.
User data:
- Income: {income}
- Expenses: {total_expenses}
- Savings: {savings}
Be succinct and give actionable advice.
"""

        return self.client.chat(system_prompt, message, temperature=0.5)
