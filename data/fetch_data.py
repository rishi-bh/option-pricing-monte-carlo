import yfinance as yf
import numpy as np

def get_annualized_volatility():
    data = yf.download("SPY", start = "2024-01-01", end = "2026-01-01", auto_adjust= True)
    
    prices = data["Close"]
    
    log_returns = np.log(
        prices / prices.shift(1)
    ).dropna()

    
    daily_volatility = log_returns.std()
    
    annualized_volatility = daily_volatility * np.sqrt(252)
    
    return float(annualized_volatility)
