"""
VERSION 9: MACD (Moving Average Convergence Divergence)
Indicateur de momentum populaire
"""

import numpy as np

price_history = []

def calculate_ema(prices, period):
    """Calcule l'EMA (Exponential Moving Average)"""
    if len(prices) < period:
        return np.mean(prices)
    
    multiplier = 2 / (period + 1)
    ema = prices[-period]  # Démarrer avec le prix initial
    
    for price in prices[-period+1:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    
    return ema

def make_decision(epoch: int, price: float):
    """Stratégie MACD"""
    price_history.append(price)
    
    base_allocation = 0.90
    
    if len(price_history) >= 35:
        # MACD = EMA12 - EMA26
        ema_12 = calculate_ema(price_history, 12)
        ema_26 = calculate_ema(price_history, 26)
        macd = ema_12 - ema_26
        
        # Signal line = EMA9 du MACD
        # Simplifié: on regarde juste le signe du MACD
        macd_pct = (macd / price) * 100
        
        # Signal haussier: MACD positif
        if macd_pct > 0.5:
            base_allocation = 0.95
        elif macd_pct > 0.1:
            base_allocation = 0.92
        # Signal baissier: MACD négatif
        elif macd_pct < -0.5:
            base_allocation = 0.75
        elif macd_pct < -0.1:
            base_allocation = 0.82
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
