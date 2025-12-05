"""
VERSION 27: Fine-tuning de V25
- Ajustement des seuils RSI/BB
- Optimisation des allocations
"""

import numpy as np

price_history = []

def calculate_atr(prices, period=14):
    if len(prices) < period + 1:
        return 0
    highs = np.maximum.accumulate(prices[-period-1:])
    lows = np.minimum.accumulate(prices[-period-1:])
    tr = highs - lows
    return np.mean(tr[-period:])

def calculate_rsi(prices, period=12):  # Légèrement plus rapide
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
    return 100 - (100 / (1 + rs))

def make_decision(epoch: int, price: float):
    price_history.append(price)
    
    base_allocation = 0.93
    
    if len(price_history) >= 24:
        rsi = calculate_rsi(price_history, period=12)
        
        ma_24 = np.mean(price_history[-24:])
        std_24 = np.std(price_history[-24:])
        z_score = (price - ma_24) / std_24 if std_24 > 0 else 0
        
        # RSI signal optimisé
        rsi_signal = 0
        if rsi < 25:
            rsi_signal = 2
        elif rsi < 40:
            rsi_signal = 1
        elif rsi > 75:
            rsi_signal = -2
        elif rsi > 60:
            rsi_signal = -1
        
        # Bollinger signal optimisé
        bb_signal = 0
        if z_score < -1.7:
            bb_signal = 2
        elif z_score < -0.65:
            bb_signal = 1
        elif z_score > 1.7:
            bb_signal = -2
        elif z_score > 0.65:
            bb_signal = -1
        
        total_signal = rsi_signal + bb_signal
        
        if total_signal >= 4:
            base_allocation = 1.0
        elif total_signal >= 3:
            base_allocation = 1.0
        elif total_signal == 2:
            base_allocation = 0.98
        elif total_signal == 1:
            base_allocation = 0.95
        elif total_signal == 0:
            base_allocation = 0.93
        elif total_signal == -1:
            base_allocation = 0.83
        elif total_signal == -2:
            base_allocation = 0.68
        elif total_signal == -3:
            base_allocation = 0.55
        elif total_signal <= -4:
            base_allocation = 0.45

    atr = calculate_atr(price_history)
    if atr > 0:
        volatility_factor = min(1.0, 0.028 / atr)
        base_allocation *= volatility_factor

    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
