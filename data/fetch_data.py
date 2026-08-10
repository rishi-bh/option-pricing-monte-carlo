import yfinance as yf
import numpy as np

def get_annualized_volatility(ticker = "SPY", start = "2024-01-01", end = "2026-01-01"):
    data = yf.download(ticker, start = start, end = end, auto_adjust= True, progress = False)
    
    prices = data["Close"]
    
    log_returns = np.log(
        prices / prices.shift(1)
    ).dropna()

    
    daily_volatility = log_returns.std()
    
    annualized_volatility = daily_volatility * np.sqrt(252)
    
    return float(annualized_volatility)
