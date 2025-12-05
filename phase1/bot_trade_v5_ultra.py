"""
VERSION 5: Stratégie Ultra-Agressive Buy & Hold+
Maximiser l'exposition avec protection minimale ultra-ciblée
"""

import numpy as np

price_history = []

def make_decision(epoch: int, price: float):
    """
    Stratégie ultra-agressive: 98% investi par défaut
    Protection UNIQUEMENT sur crash confirmé
    """
    price_history.append(price)
    
    # TRÈS haute allocation par défaut (98%)
    base_allocation = 0.98
    
    if len(price_history) >= 30:
        # Moyenne mobile courte (5 jours)
        ma_5 = np.mean(price_history[-5:])
        # Moyenne mobile longue (30 jours)
        ma_30 = np.mean(price_history[-30:])
        
        # Protection UNIQUEMENT si double signal baissier fort
        price_vs_ma5 = (price - ma_5) / ma_5
        price_vs_ma30 = (price - ma_30) / ma_30
        
        # Crash confirmé: prix < MA5 ET < MA30 de manière significative
        if price_vs_ma5 < -0.04 and price_vs_ma30 < -0.03:
            base_allocation = 0.75  # Réduction forte
        elif price_vs_ma5 < -0.02 and price_vs_ma30 < -0.015:
            base_allocation = 0.85  # Réduction modérée
        
        # Boost si forte tendance haussière
        if ma_5 > ma_30 * 1.02:  # MA5 > MA30 de 2%+
            base_allocation = 0.99
    
    allocation_asset_a = base_allocation
    allocation_cash = 1.0 - allocation_asset_a
    
    return {
        'Asset A': allocation_asset_a,
        'Cash': allocation_cash
    }
