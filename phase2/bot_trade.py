"""
Stratégie Tendance Robuste (Phase 2) - Version Sécurisée
- Conçue pour des actifs à forte autocorrélation et tendance (comme Asset B)
- Gestion des erreurs et des cas limites (NaN, 0, Crash)
- Allocation par défaut en cas de problème
"""

import numpy as np

price_history = []

def calculate_ema(prices, period):
    if len(prices) < period:
        return prices[-1]
    multiplier = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = (price - ema) * multiplier + ema
    return ema

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50
    deltas = np.diff(prices[-period-1:])
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)
    if avg_loss == 0:
        return 100
    return 100 - (100 / (1 + avg_gain / avg_loss))

def make_decision(epoch: int, price: float):
    global price_history
    
    try:
        # Sécurisation des données d'entrée
        if price is None or (isinstance(price, float) and np.isnan(price)):
            if price_history:
                price = price_history[-1]
            else:
                price = 100.0 # Valeur arbitraire pour éviter le crash au démarrage
        
        price_history.append(price)
        
        # Allocation de base élevée car l'actif est structurellement haussier
        allocation = 0.90
        
        if len(price_history) >= 50:
            # Indicateurs de tendance
            ema_20 = calculate_ema(price_history[-30:], 20)
            ema_50 = calculate_ema(price_history[-60:], 50)
            
            # Indicateur de momentum
            rsi = calculate_rsi(price_history, 14)
            
            # Momentum simple (ROC)
            prev_price_roc = price_history[-11]
            if prev_price_roc == 0:
                roc_10 = 0
            else:
                roc_10 = (price - prev_price_roc) / prev_price_roc
            
            score = 0
            
            # 1. Tendance EMA (Le plus important)
            if price > ema_20:
                score += 2
            elif price > ema_50:
                score += 1
            else:
                score -= 1
                
            # 2. Croisement EMA (Golden Cross confirmation)
            if ema_20 > ema_50:
                score += 1
            
            # 3. RSI (Confirmation de momentum)
            if rsi > 55:
                score += 1
            elif rsi < 45:
                score -= 1
                
            # 4. ROC (Vitesse)
            if roc_10 > 0:
                score += 1
            
            # Allocation dynamique
            if score >= 4:
                allocation = 1.0      # Tendance très forte
            elif score >= 3:
                allocation = 0.98     # Tendance forte
            elif score >= 1:
                allocation = 0.95     # Tendance modérée
            elif score >= -1:
                allocation = 0.85     # Incertain / Consolidation
            else:
                allocation = 0.10     # Tendance baissière (Protection)

        # Sécurisation de l'allocation
        allocation = max(0.0, min(1.0, allocation))

        return {
            'Asset B': allocation,
            'Cash': 1.0 - allocation
        }
        
    except Exception:
        # En cas de crash imprévu, on reste investi à 50% pour ne pas avoir 0 PnL
        return {
            'Asset B': 0.5,
            'Cash': 0.5
        }
