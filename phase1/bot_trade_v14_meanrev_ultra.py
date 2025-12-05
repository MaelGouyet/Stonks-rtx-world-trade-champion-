"""
VERSION 14: Mean Reversion ULTRA-OPTIMISÉE
Bollinger Bands avec paramètres optimisés et multi-seuils
"""

import numpy as np

price_history = []

def make_decision(epoch: int, price: float):
    """Mean reversion optimisée avec seuils affinés"""
    price_history.append(price)
    
    base_allocation = 0.91
    
    if len(price_history) >= 25:
        # Bollinger Bands optimisées (25 jours au lieu de 20)
        ma_25 = np.mean(price_history[-25:])
        std_25 = np.std(price_history[-25:])
        
        if std_25 > 0:
            # Z-score normalisé
            z_score = (price - ma_25) / std_25
            
            # Seuils ultra-optimisés
            if z_score < -1.8:  # Extrêmement bas
                base_allocation = 0.98
            elif z_score < -1.2:  # Très bas
                base_allocation = 0.96
            elif z_score < -0.6:  # Bas
                base_allocation = 0.93
            elif z_score > 1.8:  # Extrêmement haut
                base_allocation = 0.68
            elif z_score > 1.2:  # Très haut
                base_allocation = 0.75
            elif z_score > 0.6:  # Haut
                base_allocation = 0.83
            
            # Confirmation: tendance générale
            ma_50 = np.mean(price_history[-min(50, len(price_history)):])
            if price > ma_50:  # Tendance haussière globale
                base_allocation = min(base_allocation * 1.03, 0.99)
    
    return {
        'Asset A': base_allocation,
        'Cash': 1.0 - base_allocation
    }
