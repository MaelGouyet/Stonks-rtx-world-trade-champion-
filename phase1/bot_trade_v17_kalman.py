"""
VERSION 17: Kalman Filter Inspired - Adaptive Signal Processing
Uses exponential smoothing with adaptive parameters
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

def calculate_ema(prices, period):
    """Exponential Moving Average"""
    if len(prices) < period:
        return np.mean(prices)
    
    multiplier = 2 / (period + 1)
    ema = prices[-period]
    
    for price in prices[-period+1:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    
    return ema

def make_decision(epoch: int, price: float):
    """Advanced signal processing with adaptive filtering"""
    price_history.append(price)
    
    base_allocation = 0.92
    
    if len(price_history) >= 30:
        # Multi-EMA system for trend detection
        ema_8 = calculate_ema(price_history, 8)
        ema_21 = calculate_ema(price_history, 21)
        ema_50 = calculate_ema(price_history, 50) if len(price_history) >= 50 else ema_21
        
        # RSI for momentum
        rsi = calculate_rsi(price_history, period=14)
        
        # Bollinger-like bands
        ma_20 = np.mean(price_history[-20:])
        std_20 = np.std(price_history[-20:])
        z_score = (price - ma_20) / std_20 if std_20 > 0 else 0
        
        # === SIGNAL FUSION ===
        signal_score = 0
        
        # 1. EMA Trend (40% weight)
        if ema_8 > ema_21 > ema_50:
            signal_score += 2.0  # Strong uptrend
        elif ema_8 > ema_21:
            signal_score += 1.0  # Uptrend
        elif ema_8 < ema_21 < ema_50:
            signal_score -= 2.0  # Strong downtrend
        elif ema_8 < ema_21:
            signal_score -= 1.0  # Downtrend
        
        # 2. RSI Momentum (30% weight)
        if rsi < 25:
            signal_score += 1.5
        elif rsi < 35:
            signal_score += 0.8
        elif rsi > 75:
            signal_score -= 1.5
        elif rsi > 65:
            signal_score -= 0.8
        
        # 3. Bollinger Z-score (30% weight)
        if z_score < -1.8:
            signal_score += 1.5
        elif z_score < -1.0:
            signal_score += 0.8
        elif z_score > 1.8:
            signal_score -= 1.5
        elif z_score > 1.0:
            signal_score -= 0.8
        
        # Convert signal to allocation (0.65 to 0.99)
        # signal_score ranges roughly -5 to +5
        normalized_signal = np.clip(signal_score / 5.0, -1, 1)
        base_allocation = 0.82 + (normalized_signal * 0.17)
        
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
