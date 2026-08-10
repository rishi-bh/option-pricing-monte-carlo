import numpy as np
from data.fetch_data import get_annualized_volatility
from models.black_scholes import black_scholes_call
from models.monte_carlo import antithetic_monte_carlo_call, monte_carlo_call
from utils.plotting import plot_convergence


def main():
    np.random.seed(42)
    # 1. Fetch Volatility & Set Parameters
    windows = ["3mo", "6mo", "1y", "2y", "5y"]
    for window in windows:
        sigma = get_annualized_volatility(ticker="SPY", period=window)
        print(f"{window}: "f"{sigma:.2%}")

    S0, K, r, T = 100.0, 100.0, 0.05, 1.0
    
    print(f"Annualized Volatility (SPY): {sigma:.4f}")
    
    # 2. Run Benchmarks
    bs_price = black_scholes_call(S0, K, r, sigma, T)
    mc_price, mc_se = monte_carlo_call(S0, K, r, sigma, T, N=100_000)
    anti_price, anti_se = antithetic_monte_carlo_call(
        S0, K, r, sigma, T, N_pairs=100_000
    )
    
    print(f"Black-Scholes Price: ${bs_price:.4f}")
    print(f"Standard MC Price:   ${mc_price:.4f} (SE: {mc_se:.6f})")
    print(f"Antithetic MC Price: ${anti_price:.4f} (SE: {anti_se:.6f})")
    
    # 3. Generate Convergence Data
    counts = np.logspace(2, 5, num=50, dtype=int)
    mc_curve, anti_curve = [], []
    
    for n in counts:
        mc_p, _ = monte_carlo_call(S0, K, r, sigma, T, N=2 * n)
        anti_p, _ = antithetic_monte_carlo_call(S0, K, r, sigma, T, N_pairs=n)
        mc_curve.append(mc_p)
        anti_curve.append(anti_p)
    
    #4. Variance + Error Calculations
    variance_reduction = (1 - (anti_se / mc_se) ** 2) * 100
    print(f"Variance Reduction: {variance_reduction:.2f}%")
    
    mc_error = abs(mc_price - bs_price)
    anti_error = abs(anti_price - bs_price)
    print(f"Standard MC Error:   ${mc_error:.4f}")
    print(f"Antithetic MC Error: ${anti_error:.4f}")
    
    # 5. Plot
    plot_convergence(counts, mc_curve, anti_curve, bs_price)

if __name__ == "__main__":
    main()
