"""
VERSION 5: Enhanced Momentum with Volatility Filter
Add volatility adjustment to momentum strategy
"""

import numpy as np

price_history = []

def calculate_momentum(prices, period):
    if len(prices) < period:
        return 0
    return (prices[-1] - prices[-period]) / prices[-period]

def make_decision(epoch: int, price: float):
    price_history.append(price)
    base_allocation = 0.95
    
    if len(price_history) >= 30:
        # Multi-timeframe momentum
        mom_8 = calculate_momentum(price_history, 8)
        mom_18 = calculate_momentum(price_history, 18)
        mom_30 = calculate_momentum(price_history, 30)
        avg_mom = (mom_8 + mom_18 + mom_30) / 3
        
        # Volatility adjustment
        recent_prices = np.array(price_history[-21:])
        recent_returns = np.diff(recent_prices) / recent_prices[:-1]
        volatility = np.std(recent_returns)
        
        # Adjust thresholds based on volatility
        high_vol_multiplier = 1.2 if volatility > 0.01 else 1.0
        
        if avg_mom > 0.02 * high_vol_multiplier:
            base_allocation = 0.99
        elif avg_mom > 0.01 * high_vol_multiplier:
            base_allocation = 0.97
        elif avg_mom > 0:
            base_allocation = 0.94
        elif avg_mom > -0.01:
            base_allocation = 0.88
        else:
            base_allocation = 0.75
    
    return {'Asset B': base_allocation, 'Cash': 1.0 - base_allocation}
