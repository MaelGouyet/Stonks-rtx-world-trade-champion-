"""
VERSION 7: Momentum with Trend Strength
Add trend strength indicator to momentum
"""

import numpy as np

price_history = []

def calculate_momentum(prices, period):
    if len(prices) < period:
        return 0
    return (prices[-1] - prices[-period]) / prices[-period]

def calculate_trend_strength(prices, period=20):
    """Measure how linear the trend is"""
    if len(prices) < period:
        return 0
    recent = prices[-period:]
    x = np.arange(len(recent))
    correlation = np.corrcoef(x, recent)[0, 1]
    return correlation

def make_decision(epoch: int, price: float):
    price_history.append(price)
    base_allocation = 0.95
    
    if len(price_history) >= 30:
        # Multi-timeframe momentum
        mom_8 = calculate_momentum(price_history, 8)
        mom_18 = calculate_momentum(price_history, 18)
        mom_30 = calculate_momentum(price_history, 30)
        avg_mom = (mom_8 + mom_18 + mom_30) / 3
        
        # Trend strength (correlation with time)
        trend_strength = calculate_trend_strength(price_history, 20)
        
        # Boost allocation when trend is strong and consistent
        if avg_mom > 0.015 and trend_strength > 0.7:
            # Strong consistent uptrend
            base_allocation = 0.99
        elif avg_mom > 0.01 and trend_strength > 0.5:
            base_allocation = 0.98
        elif avg_mom > 0.01:
            base_allocation = 0.97
        elif avg_mom > 0:
            base_allocation = 0.93
        elif avg_mom > -0.01:
            base_allocation = 0.88
        else:
            base_allocation = 0.75
    
    return {'Asset B': base_allocation, 'Cash': 1.0 - base_allocation}
