"""
VERSION 19: Machine Learning Inspired - Feature Engineering
Uses multiple derived features with optimized thresholds
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

def calculate_roc(prices, period):
    """Rate of Change"""
    if len(prices) < period + 1:
        return 0
    return (prices[-1] / prices[-period-1] - 1) * 100

def calculate_williams_r(prices, period=14):
    """Williams %R oscillator"""
    if len(prices) < period:
        return -50
    
    recent = prices[-period:]
    highest = max(recent)
    lowest = min(recent)
    current = prices[-1]
    
    if highest == lowest:
        return -50
    
    wr = -100 * (highest - current) / (highest - lowest)
    return wr

def make_decision(epoch: int, price: float):
    """ML-inspired multi-feature strategy"""
    price_history.append(price)
    
    base_allocation = 0.91
    
    if len(price_history) >= 30:
        # === FEATURE ENGINEERING ===
        
        # Feature 1: RSI
        rsi = calculate_rsi(price_history, period=14)
        rsi_normalized = (rsi - 50) / 50  # Normalize to [-1, 1]
        
        # Feature 2: Bollinger Z-Score
        ma_20 = np.mean(price_history[-20:])
        std_20 = np.std(price_history[-20:])
        z_score = (price - ma_20) / std_20 if std_20 > 0 else 0
        z_normalized = np.clip(z_score / 2.5, -1, 1)
        
        # Feature 3: Multiple ROC (momentum)
        roc_5 = calculate_roc(price_history, 5)
        roc_10 = calculate_roc(price_history, 10)
        roc_20 = calculate_roc(price_history, 20)
        momentum_composite = (roc_5 * 0.5 + roc_10 * 0.3 + roc_20 * 0.2) / 3
        momentum_normalized = np.clip(momentum_composite, -1, 1)
        
        # Feature 4: Williams %R
        williams = calculate_williams_r(price_history, 14)
        williams_normalized = williams / 100  # Already in [-100, 0]
        
        # Feature 5: Volatility regime
        returns = np.diff(price_history[-20:]) / price_history[-21:-1]
        volatility = np.std(returns)
        vol_threshold = 0.0092  # Historical average
        vol_factor = 1.0 if volatility < vol_threshold else 0.85
        
        # === WEIGHTED FEATURE COMBINATION ===
        # Inverse signals for mean reversion indicators (z_score)
        buy_signal = (
            (-z_normalized * 0.30) +     # Mean reversion (inverse)
            (-rsi_normalized * 0.25) +    # Mean reversion (inverse)
            (momentum_normalized * 0.25) + # Momentum (direct)
            (-williams_normalized * 0.20)  # Mean reversion (inverse)
        )
        
        # Apply volatility adjustment
        buy_signal *= vol_factor
        
        # === MAP TO ALLOCATION [0.65, 0.99] ===
        # buy_signal ranges roughly [-2, 2]
        allocation_center = 0.82
        allocation_range = 0.17
        
        base_allocation = allocation_center + (buy_signal * allocation_range)
        base_allocation = np.clip(base_allocation, 0.65, 0.99)
        
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
