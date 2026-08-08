def monte_carlo_call(
    S0: float, K: float, r: float, sigma: float, T: float, N: int
) -> Tuple[float, float]:
    """Standard Monte Carlo pricing for European Call Option."""
    Z = np.random.normal(0, 1, N)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    payoffs = np.maximum(ST - K, 0)
    discounted_payoffs = np.exp(-r * T) * payoffs

    price = np.mean(discounted_payoffs)
    standard_error = np.std(discounted_payoffs, ddof=1) / np.sqrt(N)
    return price, standard_error


def antithetic_monte_carlo_call(
    S0: float, K: float, r: float, sigma: float, T: float, N_pairs: int
) -> Tuple[float, float]:
    """Antithetic Variates Monte Carlo pricing for European Call Option."""
    Z = np.random.normal(0, 1, N_pairs)
    ST1 = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    ST2 = S0 * np.exp((r - 0.5 * sigma**2) * T - sigma * np.sqrt(T) * Z)

    payoffs = (np.maximum(ST1 - K, 0) + np.maximum(ST2 - K, 0)) / 2
    discounted_payoffs = np.exp(-r * T) * payoffs

    price = np.mean(discounted_payoffs)
    standard_error = np.std(discounted_payoffs, ddof=1) / np.sqrt(N_pairs)
    return price, standard_error
