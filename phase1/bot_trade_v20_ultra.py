"""
VERSION 20: Ultra-Hybrid V15 Enhanced
Takes V15 (current champion) and optimizes parameters further
"""

import numpy as np

price_history = []

def calculate_rsi(prices, period=14):
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
    """Enhanced V15 with optimized thresholds and finer granularity"""
    price_history.append(price)
    
    base_allocation = 0.91
    
    if len(price_history) >= 25:
        # RSI Signal with FINER thresholds
        rsi = calculate_rsi(price_history, period=13)  # Slightly faster RSI
        
        # Bollinger Z-score with OPTIMIZED window
        ma_23 = np.mean(price_history[-23:])  # Prime number for less harmonics
        std_23 = np.std(price_history[-23:])
        z_score = (price - ma_23) / std_23 if std_23 > 0 else 0
        
        # === ENHANCED SIGNAL SYSTEM ===
        rsi_signal = 0
        if rsi < 22:  # Extreme oversold
            rsi_signal = 2.5
        elif rsi < 28:
            rsi_signal = 2.0
        elif rsi < 35:
            rsi_signal = 1.2
        elif rsi < 43:
            rsi_signal = 0.5
        elif rsi > 78:  # Extreme overbought
            rsi_signal = -2.5
        elif rsi > 72:
            rsi_signal = -2.0
        elif rsi > 65:
            rsi_signal = -1.2
        elif rsi > 57:
            rsi_signal = -0.5
        
        bb_signal = 0
        if z_score < -2.2:  # Ultra-extreme
            bb_signal = 2.8
        elif z_score < -1.6:
            bb_signal = 2.2
        elif z_score < -1.0:
            bb_signal = 1.5
        elif z_score < -0.5:
            bb_signal = 0.7
        elif z_score > 2.2:
            bb_signal = -2.8
        elif z_score > 1.6:
            bb_signal = -2.2
        elif z_score > 1.0:
            bb_signal = -1.5
        elif z_score > 0.5:
            bb_signal = -0.7
        
        # Combined signal with adjusted weights
        total_signal = (rsi_signal * 0.45) + (bb_signal * 0.55)
        
        # === ULTRA-FINE ALLOCATION MAPPING ===
        if total_signal >= 4.5:
            base_allocation = 0.99
        elif total_signal >= 3.8:
            base_allocation = 0.97
        elif total_signal >= 3.0:
            base_allocation = 0.95
        elif total_signal >= 2.2:
            base_allocation = 0.93
        elif total_signal >= 1.5:
            base_allocation = 0.91
        elif total_signal >= 0.8:
            base_allocation = 0.89
        elif total_signal >= 0.3:
            base_allocation = 0.87
        elif total_signal >= -0.3:
            base_allocation = 0.85
        elif total_signal >= -0.8:
            base_allocation = 0.82
        elif total_signal >= -1.5:
            base_allocation = 0.78
        elif total_signal >= -2.2:
            base_allocation = 0.74
        elif total_signal >= -3.0:
            base_allocation = 0.70
        elif total_signal >= -3.8:
            base_allocation = 0.67
        else:
            base_allocation = 0.64
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
