import matplotlib.pyplot as plt
import numpy as np

def plot_convergence(
    simulation_counts, mc_results, antithetic_results, bs_price
):
    """Plot convergence curves for standard vs. antithetic Monte Carlo."""
    plt.figure(figsize=(9, 5))
    plt.plot(simulation_counts, mc_results, label="Standard Monte Carlo")
    plt.plot(
        simulation_counts,
        antithetic_results,
        label="Antithetic Monte Carlo",
    )
    plt.axhline(
        bs_price,
        color="red",
        linestyle="--",
        label="Black-Scholes Theoretical",
    )

    plt.xscale("log")
    plt.xlabel("Number of Simulation Pairs (N)")
    plt.ylabel("Option Price ($)")
    plt.title("Monte Carlo Option Pricing Convergence")
    plt.grid(True, which="major", linestyle="--", alpha=0.6)
    plt.legend()
    plt.show()
