"""
VERSION 1: Momentum Strategy for Asset B
Asset B characteristics: +120% return, 0.53% volatility, 0.35 autocorrelation
Strong uptrend with momentum - use trend following
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
    rsi = 100 - (100 / (1 + rs))
    return rsi

def make_decision(epoch: int, price: float):
    """
    Momentum strategy: ride the trend with high allocation
    Reduce only on strong overbought signals
    """
    price_history.append(price)
    
    # Default: Stay heavily invested (strong uptrend)
    base_allocation = 0.95
    
    if len(price_history) >= 20:
        # RSI for overbought/oversold
        rsi = calculate_rsi(price_history, period=14)
        
        # EMA trend
        ema_10 = np.mean(price_history[-10:])
        ema_20 = np.mean(price_history[-20:])
        
        # Momentum signal
        if price > ema_10 and ema_10 > ema_20:
            # Strong uptrend - stay fully invested
            base_allocation = 0.98
        elif rsi > 75:
            # Extreme overbought - reduce slightly
            base_allocation = 0.85
        elif rsi < 30:
            # Oversold - buying opportunity
            base_allocation = 0.98
        elif price < ema_20:
            # Below long-term trend - cautious
            base_allocation = 0.80
    
    return {
        'Asset B': base_allocation,
        'Cash': 1.0 - base_allocation
    }
