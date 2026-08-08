import yfinance as yf

data = yf.download("SPY", start = "2024-01-01", end = "2026-01-01", auto_adjust= True)

print(data.head())

prices = data["Close"]

log_returns = np.log(
    prices / prices.shift(1)
).dropna()

print(log_returns.head())

daily_volatility = log_returns.std()

annualized_volatility = daily_volatility * np.sqrt(252)

print(
    f"Annualized volatility: "
    f"{annualized_volatility.item():.2%}"
)
