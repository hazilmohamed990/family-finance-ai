class Recommendations:
    def analyze_receipt(self, parsed: dict, income: float = 0.0, expenses_total: float = 0.0) -> dict:
        total = parsed.get('total') or 0.0
        merchant = (parsed.get('merchant') or '').lower()
        items = parsed.get('items', [])
        necessary = False
        avoidable = False
        excessive = False
        if income and total > income * 0.2:
            excessive = True
        discretionary_keys = ['cafe', 'coffee', 'restaurant', 'bar', 'fast food', 'delivery']
        if any(k in merchant for k in discretionary_keys):
            avoidable = True
        if not excessive and not avoidable:
            necessary = True
        suggestion = ''
        if excessive:
            suggestion = 'This purchase is large relative to your income. Consider reallocating or cutting similar purchases.'
        elif avoidable:
            suggestion = 'This looks discretionary. Consider reducing frequency or choosing lower-cost alternatives.'
        else:
            suggestion = 'Purchase appears reasonable.'
        score = 0.0
        if excessive:
            score -= 0.5
        if avoidable:
            score -= 0.3
        if necessary:
            score += 0.4
        return {'necessary': necessary, 'avoidable': avoidable, 'excessive': excessive, 'suggestion': suggestion, 'score': score}
