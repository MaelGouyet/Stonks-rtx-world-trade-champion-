"""
VERSION 12: Composite Score (Ensemble de plusieurs indicateurs)
Combine RSI, Momentum, Volatilité avec pondération intelligente
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
    """Composite score de plusieurs indicateurs"""
    price_history.append(price)
    
    base_allocation = 0.90
    
    if len(price_history) >= 30:
        # === INDICATEUR 1: RSI (40%) ===
        rsi = calculate_rsi(price_history, period=14)
        rsi_score = 0
        if rsi < 30:
            rsi_score = 1.0
        elif rsi < 45:
            rsi_score = 0.3
        elif rsi > 70:
            rsi_score = -1.0
        elif rsi > 55:
            rsi_score = -0.3
        
        # === INDICATEUR 2: Momentum (30%) ===
        ma_5 = np.mean(price_history[-5:])
        ma_20 = np.mean(price_history[-20:])
        momentum_score = 0
        if ma_5 > ma_20 * 1.01:  # MA5 > MA20 de 1%+
            momentum_score = 0.8
        elif ma_5 > ma_20:
            momentum_score = 0.3
        elif ma_5 < ma_20 * 0.99:
            momentum_score = -0.8
        elif ma_5 < ma_20:
            momentum_score = -0.3
        
        # === INDICATEUR 3: Position vs MA long terme (20%) ===
        ma_30 = np.mean(price_history[-30:])
        position_score = 0
        price_vs_ma = (price - ma_30) / ma_30
        if price_vs_ma > 0.02:
            position_score = 0.7
        elif price_vs_ma > 0:
            position_score = 0.2
        elif price_vs_ma < -0.02:
            position_score = -0.7
        else:
            position_score = -0.2
        
        # === INDICATEUR 4: Volatilité (10%) ===
        returns = np.diff(price_history[-20:]) / price_history[-21:-1]
        volatility = np.std(returns)
        vol_score = 0
        if volatility < 0.008:  # Basse volatilité
            vol_score = 0.5
        elif volatility > 0.012:  # Haute volatilité
            vol_score = -0.5
        
        # === SCORE COMPOSITE ===
        total_score = (
            rsi_score * 0.40 +
            momentum_score * 0.30 +
            position_score * 0.20 +
            vol_score * 0.10
        )
        
        # Conversion score [-1, 1] → allocation [0.70, 0.97]
        base_allocation = 0.835 + (total_score * 0.135)
        base_allocation = np.clip(base_allocation, 0.70, 0.97)
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
