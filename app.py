import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf

from data.fetch_data import get_annualized_volatility
from models.black_scholes import black_scholes_call
from models.monte_carlo import monte_carlo_call, antithetic_monte_carlo_call

st.title("Monte Carlo Option Pricer (SPY, at-the-money call)")

# 1. Controls the visitor can change
days = st.selectbox("Volatility window (days)", [30, 60, 90, 180, 252], index=4)
n = st.slider("Number of simulations", 1_000, 200_000, 100_000, step=1_000)

# 2. Same setup as your main.py
spy = yf.download("SPY", period="5d", progress=False, multi_level_index=False)
S0 = float(spy["Close"].iloc[-1])
K, r, T = S0, 0.05, 1.0
sigma = get_annualized_volatility(ticker="SPY", days=days)

bs = black_scholes_call(S0, K, r, sigma, T)
mc, mc_se = monte_carlo_call(S0, K, r, sigma, T, N=n)
anti, anti_se = antithetic_monte_carlo_call(S0, K, r, sigma, T, N_pairs=n)

# 3. Show the numbers
st.write(f"SPY price: ${S0:.2f} | volatility: {sigma:.2%}")
st.write(f"Black-Scholes: ${bs:.4f}")
st.write(f"Monte Carlo: ${mc:.4f} (SE {mc_se:.4f})")
st.write(f"Antithetic: ${anti:.4f} (SE {anti_se:.4f})")
st.write(f"Variance reduction: {1 - (anti_se / mc_se) ** 2:.1%}")

# 4. Convergence plot
counts = np.logspace(2, 4, num=40, dtype=int)
mc_curve = [monte_carlo_call(S0, K, r, sigma, T, N=c)[0] for c in counts]
anti_curve = [antithetic_monte_carlo_call(S0, K, r, sigma, T, N_pairs=c)[0] for c in counts]

fig, ax = plt.subplots()
ax.plot(counts, mc_curve, marker="o", label="Standard Monte Carlo")
ax.plot(counts, anti_curve, marker="o", label="Antithetic Monte Carlo")
ax.axhline(bs, color="red", linestyle="--", label="Black-Scholes")
ax.set_xscale("log")
ax.set_xlabel("Simulations")
ax.set_ylabel("Option price ($)")
ax.legend()
st.pyplot(fig)
