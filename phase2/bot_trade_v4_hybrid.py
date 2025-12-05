"""
VERSION 4: Bollinger + Momentum Hybrid for Asset B
Combines Bollinger bands with momentum
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
    
    base_allocation = 0.95
    
    if len(price_history) >= 25:
        # Bollinger Bands
        ma_25 = np.mean(price_history[-25:])
        std_25 = np.std(price_history[-25:])
        z_score = (price - ma_25) / std_25 if std_25 > 0 else 0
        
        # RSI
        rsi = calculate_rsi(price_history, period=13)
        
        # Momentum
        momentum_10 = (price - price_history[-10]) / price_history[-10]
        
        # Combined signals
        if momentum_10 > 0.01 and z_score < 1.5 and rsi < 70:
            # Good momentum, not overbought
            base_allocation = 0.99
        elif momentum_10 > 0 and rsi < 60:
            # Positive momentum
            base_allocation = 0.96
        elif z_score > 2.0 or rsi > 80:
            # Extreme overbought
            base_allocation = 0.80
        elif momentum_10 < -0.02:
            # Negative momentum
            base_allocation = 0.85
    
    return {
        'Asset B': base_allocation,
        'Cash': 1.0 - base_allocation
    }
