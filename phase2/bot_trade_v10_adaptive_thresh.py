"""
VERSION 10: Adaptive Threshold Momentum
Dynamically adjust thresholds based on recent volatility
"""

import numpy as np

price_history = []

def calculate_momentum(prices, period):
    if len(prices) < period:
        return 0
    return (prices[-1] - prices[-period]) / prices[-period]

def calculate_adaptive_threshold(prices, base_threshold=0.02):
    """Adjust threshold based on recent volatility"""
    if len(prices) < 21:
        return base_threshold
    recent_prices = np.array(prices[-21:])
    recent_returns = np.diff(recent_prices) / recent_prices[:-1]
    volatility = np.std(recent_returns)
    
    # Higher volatility = higher thresholds (more conservative)
    # Lower volatility = lower thresholds (more aggressive)
    adjustment = volatility / 0.005  # Normalized around 0.5% volatility
    return base_threshold * adjustment

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
        
        # Adaptive thresholds
        thresh_high = calculate_adaptive_threshold(price_history, 0.02)
        thresh_mid = calculate_adaptive_threshold(price_history, 0.015)
        thresh_low = calculate_adaptive_threshold(price_history, 0.01)
        
        if avg_mom > thresh_high and acceleration > 0:
            base_allocation = 0.99
        elif avg_mom > thresh_mid and acceleration > 0:
            base_allocation = 0.98
        elif avg_mom > thresh_low:
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
