"""
VERSION 16: Regime Switching Strategy
Détecte automatiquement le régime de marché et adapte la stratégie
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

def detect_regime(prices):
    """Détecte le régime de marché"""
    if len(prices) < 60:
        return 'neutral'
    
    # Tendance
    ma_20 = np.mean(prices[-20:])
    ma_50 = np.mean(prices[-50:])
    trend_strength = abs(ma_20 - ma_50) / ma_50
    
    # Volatilité
    returns = np.diff(prices[-30:]) / prices[-31:-1]
    volatility = np.std(returns)
    
    # Autocorrélation (momentum vs mean reversion)
    returns_short = np.diff(prices[-20:]) / prices[-21:-1]
    autocorr = np.corrcoef(returns_short[:-1], returns_short[1:])[0, 1] if len(returns_short) > 1 else 0
    
    # Classification
    if trend_strength > 0.025 and ma_20 > ma_50:
        return 'bull_trend'
    elif trend_strength > 0.025 and ma_20 < ma_50:
        return 'bear_trend'
    elif volatility > 0.013:
        return 'high_vol'
    elif volatility < 0.007:
        return 'low_vol'
    elif abs(autocorr) < 0.1:
        return 'ranging'
    else:
        return 'neutral'

def make_decision(epoch: int, price: float):
    """Stratégie adaptative selon le régime"""
    price_history.append(price)
    
    base_allocation = 0.91
    
    if len(price_history) >= 60:
        regime = detect_regime(price_history)
        rsi = calculate_rsi(price_history, period=14)
        
        # Stratégie selon le régime
        if regime == 'bull_trend':
            # Tendance haussière: rester très investi
            base_allocation = 0.96
            if rsi < 40:
                base_allocation = 0.98
            elif rsi > 70:
                base_allocation = 0.88
        
        elif regime == 'bear_trend':
            # Tendance baissière: être prudent
            base_allocation = 0.78
            if rsi < 30:
                base_allocation = 0.90
        
        elif regime == 'ranging':
            # Range: mean reversion
            ma_20 = np.mean(price_history[-20:])
            std_20 = np.std(price_history[-20:])
            z_score = (price - ma_20) / std_20 if std_20 > 0 else 0
            
            if z_score < -1.5:
                base_allocation = 0.97
            elif z_score > 1.5:
                base_allocation = 0.73
            else:
                base_allocation = 0.90
        
        elif regime == 'high_vol':
            # Haute volatilité: être conservateur
            base_allocation = 0.82
            if rsi < 25:
                base_allocation = 0.90
        
        elif regime == 'low_vol':
            # Basse volatilité: maximiser exposition
            base_allocation = 0.95
            if rsi < 35:
                base_allocation = 0.98
        
        else:  # neutral
            # Stratégie équilibrée
            if rsi < 30:
                base_allocation = 0.95
            elif rsi > 70:
                base_allocation = 0.75
            else:
                base_allocation = 0.90
    
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
