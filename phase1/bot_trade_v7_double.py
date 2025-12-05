"""
VERSION 7: RSI avec Double Confirmation
Ajoute une confirmation de momentum court terme
"""

import numpy as np

price_history = []

def calculate_rsi(prices, period=14):
    """Calcule le RSI"""
    if len(prices) < period + 1:
        return 50
    
    deltas = np.diff(prices[-period-1:])
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def make_decision(epoch: int, price: float):
    """RSI avec double confirmation MA"""
    price_history.append(price)
    
    base_allocation = 0.92
    
    if len(price_history) >= 30:
        rsi = calculate_rsi(price_history, period=14)
        ma_20 = np.mean(price_history[-20:])
        ma_5 = np.mean(price_history[-5:])
        
        # Signal RSI
        if rsi < 30:
            base_allocation = 0.96
        elif rsi > 70:
            base_allocation = 0.72
        
        # Confirmation MA20
        if price < ma_20 * 0.97:
            base_allocation *= 0.85
        
        # Boost si tendance courte positive
        if ma_5 > ma_20 * 1.005:  # MA5 > MA20 de 0.5%+
            base_allocation = min(base_allocation * 1.05, 0.98)
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
