"""
VERSION 2: Pure Trend Following for Asset B
High allocation in uptrend, minimal trading
"""

import numpy as np

price_history = []

def make_decision(epoch: int, price: float):
    price_history.append(price)
    
    # Stay almost fully invested by default
    base_allocation = 0.97
    
    if len(price_history) >= 50:
        # Long-term moving averages
        ma_20 = np.mean(price_history[-20:])
        ma_50 = np.mean(price_history[-50:])
        
        # Simple trend following
        if price > ma_20 and ma_20 > ma_50:
            # Strong uptrend
            base_allocation = 0.99
        elif price < ma_50:
            # Below long-term trend
            base_allocation = 0.85
        elif price < ma_20:
            # Below short-term trend
            base_allocation = 0.90
    
    return {
        'Asset B': base_allocation,
        'Cash': 1.0 - base_allocation
    }
