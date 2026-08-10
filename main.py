import numpy as np
import yfinance as yf
from data.fetch_data import get_annualized_volatility
from models.black_scholes import black_scholes_call
from models.monte_carlo import antithetic_monte_carlo_call, monte_carlo_call
from utils.plotting import plot_convergence


def main():
    np.random.seed(42)
    
    ticker = "SPY"
    spy_data = yf.download(ticker, period="5d", progress=False, multi_level_index=False)
    S0 = float(spy_data["Close"].iloc[-1])
    K = S0 
    r, T = 0.05, 1.0
    windows = [30, 60, 90, 180, 252]
    counts = np.logspace(2, 4, num=40, dtype=int)
    print(f"Ticker{ticker}")
    print(f"Initial Stock Price (S0): ${S0:.2f}")
    print(f"Strike Price (K):         ${K:.2f}\n")
    print(f"{'Window':<12} {'Volatility':<12} {'BS Price':<12} {'MC Price':<12} {'Anti Price':<12}")
    print("-" * 60)

    for idx, days in enumerate(windows):
        sigma = get_annualized_volatility(ticker=ticker, days=days)
        bs_price = black_scholes_call(S0, K, r, sigma, T)
        mc_price, mc_se = monte_carlo_call(S0, K, r, sigma, T, N=100_000)
        anti_price, anti_se = antithetic_monte_carlo_call(S0, K, r, sigma, T, N_pairs=100_000)
        print(f"{days:<4} days    {sigma:<12.2%} ${bs_price:<11.4f} ${mc_price:<11.4f} ${anti_price:<11.4f}")
        mc_curve, anti_curve = [], []
        for n in counts:
            mc_p, _ = monte_carlo_call(S0, K, r, sigma, T, N=n)
            anti_p, _ = antithetic_monte_carlo_call(S0, K, r, sigma, T, N_pairs=n)
            mc_curve.append(mc_p)
            anti_curve.append(anti_p)

        plot_convergence(counts, mc_curve, anti_curve, bs_price)

    print("-" * 60 + "\n")

if __name__ == "__main__":
    main()
