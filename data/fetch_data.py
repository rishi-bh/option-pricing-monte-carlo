import yfinance as yf
import numpy as np

def get_annualized_volatility(ticker = "SPY", days = 252):
    data = yf.download(ticker, period="2y", auto_adjust= True, progress = False)
    
    prices = data["Close"].tail(days+1)
    
    log_returns = np.log(prices / prices.shift(1)).dropna()

    daily_volatility = log_returns.std()
    
    annualized_volatility = daily_volatility * np.sqrt(252)
    
    return float(annualized_volatility.item())
