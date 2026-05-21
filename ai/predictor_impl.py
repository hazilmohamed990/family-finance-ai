import numpy as np
from typing import List, Tuple

class Predictor:
    def forecast(self, months: List[str], values: List[float], horizon: int = 3) -> Tuple[List[str], List[float]]:
        if not values:
            return [f'pred-{i+1}' for i in range(horizon)], [0.0]*horizon
        if len(values) == 1:
            return [f'pred-{i+1}' for i in range(horizon)], [values[0]]*horizon
        x = np.arange(len(values))
        coeffs = np.polyfit(x, values, 1)
        next_x = np.arange(len(values), len(values) + horizon)
        preds = (coeffs[0] * next_x + coeffs[1]).tolist()
        future_months = [f'pred-{i+1}' for i in range(horizon)]
        return future_months, preds
