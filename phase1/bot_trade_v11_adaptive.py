"""
VERSION 11: Adaptive RSI avec Machine Learning simplifié
Ajuste les seuils RSI selon les conditions de marché
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

def get_market_regime(prices):
    """Détermine le régime de marché (trending vs ranging)"""
    if len(prices) < 50:
        return 'neutral'
    
    # Tendance: MA courte vs MA longue
    ma_10 = np.mean(prices[-10:])
    ma_50 = np.mean(prices[-50:])
    
    # Volatilité
    returns = np.diff(prices[-20:]) / prices[-21:-1]
    volatility = np.std(returns)
    
    trend_strength = abs(ma_10 - ma_50) / ma_50
    
    if trend_strength > 0.02:
        return 'trending'
    elif volatility < 0.008:
        return 'low_vol'
    elif volatility > 0.012:
        return 'high_vol'
    else:
        return 'ranging'

def make_decision(epoch: int, price: float):
    """RSI adaptatif selon le régime de marché"""
    price_history.append(price)
    
    base_allocation = 0.90
    
    if len(price_history) >= 50:
        rsi = calculate_rsi(price_history, period=14)
        regime = get_market_regime(price_history)
        
        # Ajuster les seuils selon le régime
        if regime == 'trending':
            # En tendance: être plus agressif
            if rsi < 35:
                base_allocation = 0.96
            elif rsi > 65:
                base_allocation = 0.78
        
        elif regime == 'ranging':
            # En range: mean reversion classique
            if rsi < 30:
                base_allocation = 0.95
            elif rsi > 70:
                base_allocation = 0.75
        
        elif regime == 'low_vol':
            # Basse volatilité: rester très investi
            base_allocation = 0.94
            if rsi < 40:
                base_allocation = 0.97
        
        elif regime == 'high_vol':
            # Haute volatilité: être plus conservateur
            base_allocation = 0.85
            if rsi > 60:
                base_allocation = 0.72
        
        # Confirmation avec MA
        ma_20 = np.mean(price_history[-20:])
        if price < ma_20 * 0.97:
            base_allocation *= 0.87
    
    elif len(price_history) >= 20:
        # Fallback simple
        rsi = calculate_rsi(price_history, period=14)
        if rsi < 30:
            base_allocation = 0.95
        elif rsi > 70:
            base_allocation = 0.75
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
