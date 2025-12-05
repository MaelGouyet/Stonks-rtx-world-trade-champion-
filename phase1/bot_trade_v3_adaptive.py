"""
VERSION 3: Stratégie Adaptive basée sur la volatilité
Pour comparer avec la version actuelle
"""

import numpy as np

price_history = []

def make_decision(epoch: int, price: float):
    """Stratégie qui s'adapte à la volatilité"""
    price_history.append(price)
    
    # Allocation très élevée par défaut
    base_allocation = 0.98
    
    if len(price_history) >= 30:
        # Calcul de la volatilité
        returns = np.diff(price_history[-20:]) / price_history[-21:-1]
        volatility = np.std(returns)
        
        # Moyenne mobile
        ma_30 = np.mean(price_history[-30:])
        
        # Si volatilité élevée ET prix en baisse
        if volatility > 0.012 and price < ma_30:
            base_allocation = 0.80
        elif volatility > 0.015:
            base_allocation = 0.75
        
        # Bonus si tendance haussière stable
        if price > ma_30 and volatility < 0.008:
            base_allocation = 0.99
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
