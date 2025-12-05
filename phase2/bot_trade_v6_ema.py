"""
VERSION 6: Exponential Moving Average Momentum
Use EMA instead of simple momentum for smoother signals
"""

import numpy as np

price_history = []

def calculate_ema(prices, period):
    if len(prices) < period:
        return np.mean(prices)
    alpha = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = alpha * p + (1 - alpha) * ema
    return ema

def make_decision(epoch: int, price: float):
    price_history.append(price)
    base_allocation = 0.95
    
    if len(price_history) >= 30:
        # EMA crossovers
        ema_8 = calculate_ema(price_history, 8)
        ema_18 = calculate_ema(price_history, 18)
        ema_30 = calculate_ema(price_history, 30)
        
        # Trend strength
        if price > ema_8 > ema_18 > ema_30:
            # Perfect alignment - strong uptrend
            base_allocation = 0.99
        elif price > ema_18 and ema_18 > ema_30:
            # Good uptrend
            base_allocation = 0.97
        elif price > ema_30:
            # Above long-term trend
            base_allocation = 0.94
        elif price < ema_30:
            # Below long-term trend
            distance = (price - ema_30) / ema_30
            if distance < -0.05:
                base_allocation = 0.75
            elif distance < -0.02:
                base_allocation = 0.85
            else:
                base_allocation = 0.90
    
    return {'Asset B': base_allocation, 'Cash': 1.0 - base_allocation}
