"""
Stratégie de Trading Quantitative - Phase 1
Algorithme : Trend Following Optimisé avec Gestion du Risque

Principe OPTIMISÉ :
- Rester très investi (95%) pour capter la tendance haussière (+8.32%)
- Réduire UNIQUEMENT lors de signaux baissiers FORTS et CONFIRMÉS
- Minimiser absolument les transactions (frais de 0.05% très pénalisants)
- Utiliser moyennes mobiles longues pour filtrer le bruit
- Protection ciblée sur les vrais drawdowns (éviter les faux signaux)

Amélioration par rapport à la version précédente:
- Allocation de base plus élevée (0.95 vs 0.85) 
- Seuils plus stricts pour éviter le sur-trading
- Signaux confirmés sur plusieurs périodes
"""

import numpy as np

# Historique global
price_history = []

def make_decision(epoch: int, price: float):
    """
    Stratégie optimisée: Maximum invested avec protection ultra-sélective.
    
    Logique:
    - Allocation par défaut: 95% (capter presque toute la hausse)
    - Réduction UNIQUEMENT si FORTE baisse confirmée
    - Éviter les faux signaux pour minimiser les transactions
    
    Parameters
    ----------
    epoch : int
        L'époque (index temporel) actuelle
    price : float
        Le prix actuel de l'Asset A
    
    Returns
    -------
    dict
        Allocation du portefeuille {'Asset A': float, 'Cash': float}
    """
    # Mise à jour de l'historique
    price_history.append(price)
    
    # Allocation de base: TRÈS investie (95%)
    base_allocation = 0.95
    
    # Signal 1: Baisse vs MA20 (moyenne mobile longue pour éviter le bruit)
    if len(price_history) >= 20:
        ma_20 = np.mean(price_history[-20:])
        price_vs_ma = (price - ma_20) / ma_20
        
        # Seuils plus stricts: réduire UNIQUEMENT si vraie tendance baissière
        if price_vs_ma < -0.05:  # Prix 5% sous MA20: baisse confirmée
            base_allocation = 0.75
        elif price_vs_ma < -0.03:  # Prix 3% sous MA20: prudence
            base_allocation = 0.85
    
    # Signal 2: Drawdown fort récent (10 jours)
    if len(price_history) >= 11:
        price_10d_ago = price_history[-11]
        recent_return = (price - price_10d_ago) / price_10d_ago
        
        # Réduire UNIQUEMENT si chute vraiment forte
        if recent_return < -0.08:  # Chute de plus de 8% en 10 jours
            base_allocation = min(base_allocation, 0.70)
        elif recent_return < -0.05:  # Chute de plus de 5% en 10 jours
            base_allocation = min(base_allocation, 0.80)
    
    # Signal 3: Trend de long terme (50 jours) - éviter de trader contre la tendance
    if len(price_history) >= 50:
        ma_50 = np.mean(price_history[-50:])
        long_term_trend = (price - ma_50) / ma_50
        
        # Si on est bien au-dessus de MA50, rester pleinement investi
        if long_term_trend > 0.02:  # Prix 2%+ au-dessus de MA50
            base_allocation = max(base_allocation, 0.90)
    
    allocation_asset_a = base_allocation
    allocation_cash = 1.0 - allocation_asset_a
    
    return {
        'Asset A': allocation_asset_a,
        'Cash': allocation_cash
    }