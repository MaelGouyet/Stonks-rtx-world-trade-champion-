"""
VERSION 8: Mean Reversion avec Bollinger Bands
Stratégie basée sur les écarts extrêmes de prix
"""

import numpy as np

price_history = []

def make_decision(epoch: int, price: float):
    """Mean reversion sur Bollinger Bands"""
    price_history.append(price)
    
    base_allocation = 0.90
    
    if len(price_history) >= 20:
        ma_20 = np.mean(price_history[-20:])
        std_20 = np.std(price_history[-20:])
        
        # Bandes de Bollinger
        upper_band = ma_20 + (2 * std_20)
        lower_band = ma_20 - (2 * std_20)
        
        # Distance normalisée du prix vs bandes
        if std_20 > 0:
            z_score = (price - ma_20) / std_20
            
            # Mean reversion: acheter quand bas, vendre quand haut
            if z_score < -1.5:  # Très en dessous (survente)
                base_allocation = 0.97
            elif z_score < -0.8:  # En dessous
                base_allocation = 0.93
            elif z_score > 1.5:  # Très au-dessus (surachat)
                base_allocation = 0.70
            elif z_score > 0.8:  # Au-dessus
                base_allocation = 0.80
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
