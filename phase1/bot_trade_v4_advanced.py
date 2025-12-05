"""
VERSION 4: Stratégie Multi-Facteurs Avancée
Combinaison optimisée de plusieurs signaux avec pondération dynamique
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

def calculate_bollinger_position(prices, window=20, num_std=2):
    """Position du prix dans les bandes de Bollinger"""
    if len(prices) < window:
        return 0.5
    
    ma = np.mean(prices[-window:])
    std = np.std(prices[-window:])
    
    upper_band = ma + (num_std * std)
    lower_band = ma - (num_std * std)
    
    current_price = prices[-1]
    
    if upper_band == lower_band:
        return 0.5
    
    # Position normalisée (0 = bande basse, 1 = bande haute)
    position = (current_price - lower_band) / (upper_band - lower_band)
    return np.clip(position, 0, 1)

def calculate_trend_strength(prices, short=10, long=50):
    """Force de la tendance basée sur plusieurs MA"""
    if len(prices) < long:
        return 0
    
    ma_short = np.mean(prices[-short:])
    ma_long = np.mean(prices[-long:])
    
    trend = (ma_short - ma_long) / ma_long
    return trend

def make_decision(epoch: int, price: float):
    """
    Stratégie multi-facteurs avancée avec pondération dynamique.
    
    Combine:
    - RSI (momentum)
    - Bollinger Bands (volatilité/extremes)
    - Trend strength (direction)
    - Volatility regime (adaptation)
    """
    price_history.append(price)
    
    # Allocation de base très élevée
    base_allocation = 0.92
    
    if len(price_history) >= 50:
        # === INDICATEURS ===
        rsi = calculate_rsi(price_history, period=14)
        bb_position = calculate_bollinger_position(price_history, window=20)
        trend = calculate_trend_strength(price_history, short=10, long=50)
        
        # Volatilité récente
        returns = np.diff(price_history[-20:]) / price_history[-21:-1]
        volatility = np.std(returns)
        
        # === SCORING SYSTEM ===
        score = 0.0
        
        # 1. RSI Score (30%)
        if rsi < 30:  # Survente
            rsi_score = 1.0
        elif rsi < 40:
            rsi_score = 0.5
        elif rsi > 70:  # Surachat
            rsi_score = -1.0
        elif rsi > 60:
            rsi_score = -0.5
        else:
            rsi_score = 0.0
        
        score += rsi_score * 0.30
        
        # 2. Bollinger Position Score (25%)
        if bb_position < 0.2:  # Près bande basse = opportunité
            bb_score = 1.0
        elif bb_position < 0.4:
            bb_score = 0.5
        elif bb_position > 0.8:  # Près bande haute = prudence
            bb_score = -0.7
        elif bb_position > 0.6:
            bb_score = -0.3
        else:
            bb_score = 0.0
        
        score += bb_score * 0.25
        
        # 3. Trend Score (25%)
        if trend > 0.03:  # Forte tendance haussière
            trend_score = 1.0
        elif trend > 0.01:
            trend_score = 0.5
        elif trend < -0.03:  # Forte tendance baissière
            trend_score = -1.0
        elif trend < -0.01:
            trend_score = -0.5
        else:
            trend_score = 0.0
        
        score += trend_score * 0.25
        
        # 4. Volatility Score (20%)
        avg_vol = 0.0092
        if volatility > avg_vol * 1.5:
            vol_score = -1.0  # Haute volatilité = réduire
        elif volatility > avg_vol * 1.2:
            vol_score = -0.5
        elif volatility < avg_vol * 0.8:
            vol_score = 0.5  # Basse volatilité = augmenter
        else:
            vol_score = 0.0
        
        score += vol_score * 0.20
        
        # === CONVERSION SCORE → ALLOCATION ===
        # Score de -1 à +1 → Allocation de 0.70 à 0.98
        allocation_range = 0.98 - 0.70
        base_allocation = 0.70 + ((score + 1) / 2) * allocation_range
        
    elif len(price_history) >= 20:
        # Moins d'indicateurs disponibles
        rsi = calculate_rsi(price_history, period=14)
        
        if rsi < 30:
            base_allocation = 0.96
        elif rsi > 70:
            base_allocation = 0.75
    
    allocation_asset_a = np.clip(base_allocation, 0.0, 1.0)
    allocation_cash = 1.0 - allocation_asset_a
    
    return {
        'Asset A': allocation_asset_a,
        'Cash': allocation_cash
    }
