"""
VERSION 15: Hybrid RSI + Bollinger (Best of Both Worlds)
Combine les meilleurs signaux de RSI et Mean Reversion
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
    """Hybride RSI + Bollinger pour double confirmation"""
    price_history.append(price)
    
    base_allocation = 0.91
    
    if len(price_history) >= 25:
        # Signal 1: RSI
        rsi = calculate_rsi(price_history, period=14)
        
        # Signal 2: Bollinger Z-score
        ma_25 = np.mean(price_history[-25:])
        std_25 = np.std(price_history[-25:])
        z_score = (price - ma_25) / std_25 if std_25 > 0 else 0
        
        # Combiner les deux signaux avec pondération
        rsi_signal = 0
        if rsi < 30:
            rsi_signal = 2  # Fort achat
        elif rsi < 45:
            rsi_signal = 1  # Achat
        elif rsi > 70:
            rsi_signal = -2  # Forte vente
        elif rsi > 55:
            rsi_signal = -1  # Vente
        
        bb_signal = 0
        if z_score < -1.5:
            bb_signal = 2
        elif z_score < -0.8:
            bb_signal = 1
        elif z_score > 1.5:
            bb_signal = -2
        elif z_score > 0.8:
            bb_signal = -1
        
        # Score composite
        total_signal = rsi_signal + bb_signal
        
        # Allocation basée sur le signal combiné
        if total_signal >= 3:  # Double confirmation achat fort
            base_allocation = 0.98
        elif total_signal == 2:
            base_allocation = 0.95
        elif total_signal == 1:
            base_allocation = 0.92
        elif total_signal == -1:
            base_allocation = 0.82
        elif total_signal == -2:
            base_allocation = 0.75
        elif total_signal <= -3:  # Double confirmation vente forte
            base_allocation = 0.68
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
