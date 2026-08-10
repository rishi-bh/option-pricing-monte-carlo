import numpy as np
from scipy.stats import norm

# Standard Monte Carlo pricing for European Call Option.
def monte_carlo_call(S0, K, r, sigma, T, N):
    Z_std = np.random.normal(0, 1, 2*N)
    
    ST_std = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z_std)
    payoffs_std = np.maximum(ST_std - K, 0)
    discounted_payoffs_std = np.exp(-r * T) * payoffs_std
    
    mc_price = np.mean(discounted_payoffs_std)
    mc_standard_error = np.std(discounted_payoffs_std, ddof=1) / np.sqrt(2*N)
    return mc_price, mc_standard_error

# Antihtetic Variates Monte Carlo pricing (N pairs = 2*N path evaluations).

def antithetic_monte_carlo_call(S0, K, r, sigma, T, N_pairs):
    Z_anti = np.random.normal(0, 1, N)
    ST1 = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z_anti)
    ST2 = S0 * np.exp((r - 0.5 * sigma**2) * T - sigma * np.sqrt(T) * Z_anti)
    
    payoff1 = np.maximum(ST1 - K, 0)
    payoff2 = np.maximum(ST2 - K, 0)
    
    average_payoffs = (payoff1 + payoff2) / 2
    discounted_antithetic_payoffs = np.exp(-r * T) * average_payoffs
    
    antithetic_price = np.mean(discounted_antithetic_payoffs)
    antithetic_standard_error = np.std(
        discounted_antithetic_payoffs, ddof=1
    ) / np.sqrt(N)
    return antithetic_price, antithetic_standard_error
