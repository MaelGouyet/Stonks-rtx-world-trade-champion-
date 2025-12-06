import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def returns_from_prices(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()

def equal_weighted(n_assets: int) -> np.ndarray:
    w = np.ones(n_assets) / n_assets
    return w

def tangency_portfolio(returns_window: pd.DataFrame, risk_free=0.0) -> np.ndarray:
    mu = returns_window.mean() * 252
    cov = returns_window.cov() * 252
    try:
        inv = np.linalg.inv(cov.values)
    except np.linalg.LinAlgError:
        inv = np.linalg.pinv(cov.values)
    excess = (mu - risk_free).values
    raw = inv.dot(excess)
    raw[raw < 0] = 0
    if raw.sum() == 0:
        raw = np.ones_like(raw)
    w = raw / raw.sum()
    return w

history = []

def make_decision(epoch: int, priceA: float, priceB: float):
    history.append({'epoch': epoch, 'priceA': priceA, 'priceB': priceB})
    df = pd.DataFrame(history).set_index('epoch')
    prices = df.rename(columns={'priceA': 'A', 'priceB': 'B'})

    if len(prices) < 2:
        return {'Asset A': 1/3, 'Asset B': 1/3, 'Cash': 1/3}

    rets = returns_from_prices(prices)
    n_assets = prices.shape[1]

    window: int = 5
    risk_free: float = 0.07

    if len(rets) < 2:
        w = equal_weighted(n_assets)
    else:
        window = min(window, len(rets))
        w = tangency_portfolio(rets.iloc[-window:], risk_free=risk_free)

    cash = max(0.0, 1.0 - w.sum())
    alloc = {'Asset A': float(w[0]), 'Asset B': float(w[1]), 'Cash': float(cash)}
    return alloc
