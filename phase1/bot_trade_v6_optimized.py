"""
VERSION 6: RSI Optimisé avec Paramètres Affinés
Optimisation fine des seuils et allocations
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
    """RSI avec paramètres optimisés"""
    price_history.append(price)
    
    # Allocation de base encore plus élevée
    base_allocation = 0.93
    
    if len(price_history) >= 20:
        rsi = calculate_rsi(price_history, period=14)
        ma_20 = np.mean(price_history[-20:])
        
        # Ajustement RSI (seuils légèrement différents)
        if rsi < 25:  # Survente extrême
            base_allocation = 0.97
        elif rsi < 35:  # Survente
            base_allocation = 0.94
        elif rsi > 75:  # Surachat extrême
            base_allocation = 0.68
        elif rsi > 65:  # Surachat
            base_allocation = 0.78
        
        # Confirmation MA (seuil ajusté)
        if price < ma_20 * 0.98:  # Prix 2%+ sous MA20
            base_allocation *= 0.88
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
