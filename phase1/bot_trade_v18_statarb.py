"""
VERSION 18: Statistical Arbitrage - Z-Score + RSI + Momentum
Triple confirmation with statistical rigor
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

def calculate_momentum_strength(prices, period=10):
    """Rate of change momentum"""
    if len(prices) < period + 1:
        return 0
    
    roc = (prices[-1] / prices[-period-1] - 1) * 100
    return roc

def make_decision(epoch: int, price: float):
    """Statistical arbitrage with triple confirmation"""
    price_history.append(price)
    
    base_allocation = 0.92
    
    if len(price_history) >= 30:
        # === INDICATOR 1: Bollinger Z-Score (35%) ===
        window = 22  # Optimized window
        ma = np.mean(price_history[-window:])
        std = np.std(price_history[-window:])
        z_score = (price - ma) / std if std > 0 else 0
        
        z_signal = 0
        if z_score < -2.0:
            z_signal = 2.5
        elif z_score < -1.3:
            z_signal = 1.5
        elif z_score < -0.7:
            z_signal = 0.5
        elif z_score > 2.0:
            z_signal = -2.5
        elif z_score > 1.3:
            z_signal = -1.5
        elif z_score > 0.7:
            z_signal = -0.5
        
        # === INDICATOR 2: RSI (35%) ===
        rsi = calculate_rsi(price_history, period=14)
        
        rsi_signal = 0
        if rsi < 25:
            rsi_signal = 2.5
        elif rsi < 32:
            rsi_signal = 1.5
        elif rsi < 42:
            rsi_signal = 0.5
        elif rsi > 75:
            rsi_signal = -2.5
        elif rsi > 68:
            rsi_signal = -1.5
        elif rsi > 58:
            rsi_signal = -0.5
        
        # === INDICATOR 3: Momentum (30%) ===
        momentum_10 = calculate_momentum_strength(price_history, 10)
        
        mom_signal = 0
        if momentum_10 > 3:
            mom_signal = 1.5
        elif momentum_10 > 1.5:
            mom_signal = 0.8
        elif momentum_10 < -3:
            mom_signal = -1.5
        elif momentum_10 < -1.5:
            mom_signal = -0.8
        
        # === COMPOSITE SIGNAL ===
        total_signal = (z_signal * 0.35) + (rsi_signal * 0.35) + (mom_signal * 0.30)
        
        # Map signal to allocation [0.65, 0.99]
        # Strong buy signals (>2) -> 0.99
        # Strong sell signals (<-2) -> 0.65
        if total_signal > 2.5:
            base_allocation = 0.99
        elif total_signal > 1.5:
            base_allocation = 0.96
        elif total_signal > 0.8:
            base_allocation = 0.93
        elif total_signal > 0.2:
            base_allocation = 0.90
        elif total_signal > -0.2:
            base_allocation = 0.87
        elif total_signal > -0.8:
            base_allocation = 0.82
        elif total_signal > -1.5:
            base_allocation = 0.76
        elif total_signal > -2.5:
            base_allocation = 0.70
        else:
            base_allocation = 0.65
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
