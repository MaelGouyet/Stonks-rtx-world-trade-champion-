"""
VERSION 10: Stochastic Oscillator
Mesure la position du prix dans son range récent
"""

import numpy as np

price_history = []

def calculate_stochastic(prices, period=14):
    """Calcule l'oscillateur stochastique"""
    if len(prices) < period:
        return 50
    
    recent_prices = prices[-period:]
    highest = max(recent_prices)
    lowest = min(recent_prices)
    current = prices[-1]
    
    if highest == lowest:
        return 50
    
    k = 100 * (current - lowest) / (highest - lowest)
    return k

def make_decision(epoch: int, price: float):
    """Stratégie Stochastic"""
    price_history.append(price)
    
    base_allocation = 0.90
    
    if len(price_history) >= 20:
        stoch = calculate_stochastic(price_history, period=14)
        
        # Stochastic < 20: survente (acheter)
        # Stochastic > 80: surachat (vendre)
        
        if stoch < 15:
            base_allocation = 0.96
        elif stoch < 25:
            base_allocation = 0.93
        elif stoch > 85:
            base_allocation = 0.72
        elif stoch > 75:
            base_allocation = 0.82
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
