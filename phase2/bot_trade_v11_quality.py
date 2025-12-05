"""
VERSION 11: Momentum Quality Score
Combine multiple quality indicators for momentum
"""

import numpy as np

price_history = []

def calculate_momentum(prices, period):
    if len(prices) < period:
        return 0
    return (prices[-1] - prices[-period]) / prices[-period]

def calculate_momentum_quality(prices, period=20):
    """Measure quality of momentum trend"""
    if len(prices) < period:
        return 0
    
    recent = prices[-period:]
    # Linear regression correlation
    x = np.arange(len(recent))
    correlation = np.corrcoef(x, recent)[0, 1]
    
    # Consistency: % of positive moves
    moves = np.diff(recent)
    consistency = np.sum(moves > 0) / len(moves) if len(moves) > 0 else 0.5
    
    # Combined quality score
    return (correlation + consistency) / 2

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
        
        # Momentum quality
        quality = calculate_momentum_quality(price_history, 20)
        
        # High quality momentum deserves higher allocation
        quality_boost = 0.0
        if quality > 0.7:
            quality_boost = 0.01  # Add 1% to allocation
        
        if avg_mom > 0.02 and acceleration > 0:
            base_allocation = min(0.99, 0.99 + quality_boost)
        elif avg_mom > 0.015 and acceleration > 0 and quality > 0.6:
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
            base_allocation = 0.70
        else:
            base_allocation = 0.75
    
    return {'Asset B': base_allocation, 'Cash': 1.0 - base_allocation}
