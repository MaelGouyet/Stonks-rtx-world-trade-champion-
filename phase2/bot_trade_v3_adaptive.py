"""
VERSION 3: Adaptive Momentum for Asset B
Uses momentum strength to adjust allocation
"""

import numpy as np

price_history = []

def calculate_momentum(prices, period=20):
    if len(prices) < period:
        return 0
    return (prices[-1] - prices[-period]) / prices[-period]

def make_decision(epoch: int, price: float):
    price_history.append(price)
    
    base_allocation = 0.95
    
    if len(price_history) >= 30:
        # Multiple momentum timeframes
        mom_10 = calculate_momentum(price_history, 10)
        mom_20 = calculate_momentum(price_history, 20)
        mom_30 = calculate_momentum(price_history, 30)
        
        # Average momentum
        avg_mom = (mom_10 + mom_20 + mom_30) / 3
        
        if avg_mom > 0.02:
            # Strong positive momentum
            base_allocation = 0.99
        elif avg_mom > 0.01:
            # Moderate positive momentum
            base_allocation = 0.97
        elif avg_mom > 0:
            # Weak positive momentum
            base_allocation = 0.93
        elif avg_mom > -0.01:
            # Weak negative momentum
            base_allocation = 0.88
        else:
            # Strong negative momentum
            base_allocation = 0.75
    
    return {
        'Asset B': base_allocation,
        'Cash': 1.0 - base_allocation
    }
