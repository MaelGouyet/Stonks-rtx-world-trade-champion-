"""
VERSION 21: GRID-OPTIMIZED Hybrid - RSI(13) + Bollinger(25)
Grid search winner with Score: 0.0392, PnL: +14.64%
"""

import numpy as np

price_history = []

def calculate_rsi(prices, period=13):
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
    base_allocation = 0.91
    
    if len(price_history) >= 25:
        rsi = calculate_rsi(price_history, period=13)
        ma = np.mean(price_history[-25:])
        std = np.std(price_history[-25:])
        z_score = (price - ma) / std if std > 0 else 0
        
        rsi_signal = 0
        if rsi < 30:
            rsi_signal = 2
        elif rsi < 45:
            rsi_signal = 1
        elif rsi > 70:
            rsi_signal = -2
        elif rsi > 55:
            rsi_signal = -1
        
        bb_signal = 0
        if z_score < -1.5:
            bb_signal = 2
        elif z_score < -0.8:
            bb_signal = 1
        elif z_score > 1.5:
            bb_signal = -2
        elif z_score > 0.8:
            bb_signal = -1
        
        total_signal = rsi_signal + bb_signal
        
        if total_signal >= 3:
            base_allocation = 0.98
        elif total_signal == 2:
            base_allocation = 0.95
        elif total_signal == 1:
            base_allocation = 0.92
        elif total_signal == -1:
            base_allocation = 0.82
        elif total_signal == -2:
            base_allocation = 0.75
        elif total_signal <= -3:
            base_allocation = 0.68
    
    return {'Asset A': base_allocation, 'Cash': 1.0 - base_allocation}
