"""
VERSION 12: Fine-tuned Allocation Levels
Optimize the exact allocation percentages
"""

import numpy as np

price_history = []

def calculate_momentum(prices, period):
    if len(prices) < period:
        return 0
    return (prices[-1] - prices[-period]) / prices[-period]

def make_decision(epoch: int, price: float):
    price_history.append(price)
    base_allocation = 0.96  # Slightly higher baseline
    
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
        
        # Fine-tuned allocation levels
        if avg_mom > 0.022 and acceleration > 0.001:
            base_allocation = 0.995  # Maximum exposure
        elif avg_mom > 0.018 and acceleration > 0:
            base_allocation = 0.985
        elif avg_mom > 0.012:
            base_allocation = 0.975
        elif avg_mom > 0.005:
            base_allocation = 0.945
        elif avg_mom > 0:
            base_allocation = 0.920
        elif avg_mom > -0.008:
            base_allocation = 0.880
        elif acceleration < -0.012:
            base_allocation = 0.680
        else:
            base_allocation = 0.730
    
    return {'Asset B': base_allocation, 'Cash': 1.0 - base_allocation}
