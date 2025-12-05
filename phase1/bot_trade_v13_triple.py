"""
VERSION 13: Triple Momentum avec Filtre de Volatilité
Combine 3 timeframes de momentum avec protection intelligente
"""

import numpy as np

price_history = []

def make_decision(epoch: int, price: float):
    """Triple momentum multi-timeframe"""
    price_history.append(price)
    
    base_allocation = 0.92
    
    if len(price_history) >= 60:
        # Momentum 3 timeframes
        ma_5 = np.mean(price_history[-5:])
        ma_20 = np.mean(price_history[-20:])
        ma_50 = np.mean(price_history[-50:])
        
        # Score momentum (tous positifs = fort momentum)
        momentum_score = 0
        if ma_5 > ma_20:
            momentum_score += 1
        if ma_20 > ma_50:
            momentum_score += 1
        if price > ma_5:
            momentum_score += 1
        
        # Allocation selon momentum
        if momentum_score == 3:  # Triple confirmation
            base_allocation = 0.97
        elif momentum_score == 2:
            base_allocation = 0.92
        elif momentum_score == 1:
            base_allocation = 0.82
        else:  # momentum_score == 0 (tout négatif)
            base_allocation = 0.70
        
        # Filtre volatilité
        returns = np.diff(price_history[-20:]) / price_history[-21:-1]
        volatility = np.std(returns)
        
        # Si volatilité extrême, réduire
        if volatility > 0.015:
            base_allocation *= 0.85
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
