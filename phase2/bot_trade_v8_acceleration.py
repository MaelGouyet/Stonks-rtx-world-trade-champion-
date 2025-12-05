"""
VERSION 8: Momentum with Acceleration
Add rate of change of momentum (acceleration)
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
    
    if len(price_history) >= 40:
        # Multi-timeframe momentum
        mom_8 = calculate_momentum(price_history, 8)
        mom_18 = calculate_momentum(price_history, 18)
        mom_30 = calculate_momentum(price_history, 30)
        avg_mom = (mom_8 + mom_18 + mom_30) / 3
        
        # Momentum acceleration (momentum of momentum)
        # Compare recent momentum to past momentum
        mom_recent = (mom_8 + mom_18) / 2
        mom_past_8 = calculate_momentum(price_history[:-5], 8)
        mom_past_18 = calculate_momentum(price_history[:-5], 18)
        mom_past = (mom_past_8 + mom_past_18) / 2
        
        acceleration = mom_recent - mom_past
        
        # Higher allocation when both momentum and acceleration positive
        if avg_mom > 0.02 and acceleration > 0:
            base_allocation = 0.99
        elif avg_mom > 0.015 and acceleration > 0:
            base_allocation = 0.98
        elif avg_mom > 0.01:
            base_allocation = 0.97
        elif avg_mom > 0:
            base_allocation = 0.93
        elif avg_mom > -0.01:
            base_allocation = 0.88
        elif acceleration < -0.01:
            # Strong deceleration
            base_allocation = 0.70
        else:
            base_allocation = 0.75
    
    return {'Asset B': base_allocation, 'Cash': 1.0 - base_allocation}
