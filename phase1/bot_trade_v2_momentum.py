"""
VERSION 2: Stratégie Momentum avec RSI
Pour comparer avec la version actuelle
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
    """Stratégie basée sur RSI et tendance"""
    price_history.append(price)
    
    # Allocation de base élevée
    base_allocation = 0.90
    
    if len(price_history) >= 20:
        rsi = calculate_rsi(price_history, period=14)
        ma_20 = np.mean(price_history[-20:])
        
        # Augmenter en zone de survente
        if rsi < 30:
            base_allocation = 0.95
        # Réduire en zone de surachat
        elif rsi > 70:
            base_allocation = 0.70
        
        # Confirmer avec MA
        if price < ma_20 * 0.97:  # Prix 3% sous MA20
            base_allocation *= 0.85
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
