"""
Stratégie Prime V4 (Phase 1) - Hybrid RSI + Bollinger
- Combine RSI et Bollinger Bands pour une précision chirurgicale
- Vente totale sur double signal de surachat
- Achat total sur double signal de survente
"""

import numpy as np

price_history = []

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

def calculate_bb(prices, period=20, std_dev=2.0):
    if len(prices) < period:
        return prices[-1], prices[-1], prices[-1]
    sma = np.mean(prices[-period:])
    std = np.std(prices[-period:])
    return sma, sma + std_dev * std, sma - std_dev * std

def make_decision(epoch: int, price: float):
    global price_history
    
    # Sécurisation
    if price is None or (isinstance(price, float) and np.isnan(price)):
        if price_history:
            price = price_history[-1]
        else:
            price = 100.0
            
    price_history.append(price)
    
    # Base Allocation
    allocation = 0.85
    
    if len(price_history) >= 20:
        rsi = calculate_rsi(price_history, 14)
        sma, upper, lower = calculate_bb(price_history, 20, 2.0)
        
        # Score de surachat / survente
        score = 0
        
        # RSI
        if rsi > 70: score -= 2
        elif rsi > 60: score -= 1
        elif rsi < 30: score += 2
        elif rsi < 40: score += 1
            
        # Bollinger
        if price > upper: score -= 2
        elif price > sma + (upper - sma) * 0.5: score -= 1
        elif price < lower: score += 2
        elif price < sma - (sma - lower) * 0.5: score += 1
            
        # Décision finale
        if score <= -3:
            allocation = 0.0   # Vente Totale (Double signal fort)
        elif score <= -1:
            allocation = 0.20  # Vente partielle
        elif score >= 3:
            allocation = 1.0   # Achat Total (Double signal fort)
        elif score >= 1:
            allocation = 0.95  # Achat fort
        else:
            allocation = 0.85  # Neutre (Base)

    return {
        'Asset A': allocation,
        'Cash': 1.0 - allocation
    }
