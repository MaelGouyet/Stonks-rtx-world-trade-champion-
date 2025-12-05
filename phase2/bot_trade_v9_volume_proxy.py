"""
VERSION 9: Triple Momentum with Volume Proxy
Add price spread analysis as volume proxy
"""

import numpy as np

price_history = []

def calculate_momentum(prices, period):
    if len(prices) < period:
        return 0
    return (prices[-1] - prices[-period]) / prices[-period]

def calculate_price_spread(prices, period=10):
    """Price spread as proxy for volume/activity"""
    if len(prices) < period:
        return 0
    high = np.max(prices[-period:])
    low = np.min(prices[-period:])
    return (high - low) / np.mean(prices[-period:])

def make_decision(epoch: int, price: float):
    price_history.append(price)
    base_allocation = 0.95
    
    if len(price_history) >= 40:
        mom_8 = calculate_momentum(price_history, 8)
        mom_16 = calculate_momentum(price_history, 16)
        mom_28 = calculate_momentum(price_history, 28)
        avg_mom = (mom_8 + mom_16 + mom_28) / 3
        
        # Acceleration
        mom_recent = (mom_8 + mom_16) / 2
        mom_past_8 = calculate_momentum(price_history[:-6], 8)
        mom_past_16 = calculate_momentum(price_history[:-6], 16)
        mom_past = (mom_past_8 + mom_past_16) / 2
        acceleration = mom_recent - mom_past
        
        # Price spread (volatility/activity)
        spread = calculate_price_spread(price_history, 10)
        
        # Boost allocation when spread is low (consolidation before breakout)
        spread_multiplier = 1.0
        if spread < 0.02:  # Low volatility
            spread_multiplier = 1.1
        
        if avg_mom > 0.02 * spread_multiplier and acceleration > 0:
            base_allocation = 0.99
        elif avg_mom > 0.015 * spread_multiplier and acceleration > 0:
            base_allocation = 0.98
        elif avg_mom > 0.01:
            base_allocation = 0.97
        elif avg_mom > 0:
            base_allocation = 0.93
        elif avg_mom > -0.01:
            base_allocation = 0.88
        elif acceleration < -0.01:
            base_allocation = 0.70
        else:
            base_allocation = 0.75
    
    return {'Asset B': base_allocation, 'Cash': 1.0 - base_allocation}
