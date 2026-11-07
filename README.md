# Monte Carlo Option Pricing Engine

**[Live demo](https://option-pricing-monte-carlo.streamlit.app/)** | Python | NumPy | SciPy | Streamlit

A Python Monte Carlo engine for pricing European call options using historical volatility estimates. It benchmarks simulated prices against the closed-form Black-Scholes solution and measures how Antithetic Variates improve Monte Carlo accuracy at equal compute.

## Results at a glance

Example run: at-the-money SPY call (strike = spot), risk-free rate 5%, 1-year maturity, 100,000 simulations per estimator.

| Estimator | Price | Absolute error vs. Black-Scholes | Standard error |
|---|---|---|---|
| Black-Scholes (benchmark) | \$9.0668 | n/a | n/a |
| Standard Monte Carlo | \$9.0773 | \$0.0105 (0.12%) | \$0.026913 |
| Antithetic Monte Carlo | \$9.0663 | \$0.0005 (0.006%) | \$0.017939 |

* **Variance reduction: 55.6%** (equivalently, standard error is 33% lower).
* A 55.6% variance reduction means the antithetic estimator matches the accuracy of a standard estimator using over 2x as many draws.
* The comparison is at equal compute: `N` antithetic pairs cost the same 2N payoff evaluations as 2N independent standard draws.

These figures come from a single unseeded run, so exact values change slightly between runs.

![Monte Carlo convergence comparison](https://github.com/user-attachments/assets/15c39d64-13a5-4d0f-b01d-09f1b75689a5)

*Convergence of standard vs. antithetic Monte Carlo toward the Black-Scholes price as the number of simulations grows (100 to 10,000).*

## Try it

* **Live app:** [option-pricing-monte-carlo.streamlit.app](https://option-pricing-monte-carlo.streamlit.app/) lets you change the volatility window and number of simulations and see prices, standard errors and the convergence plot update. If the app has been idle, it may need a few seconds to wake up.
* **Run locally:** see [Installation](#installation) and [Usage](#usage).

## Overview

Monte Carlo methods give a flexible way to price derivatives by simulating the underlying asset's future price and averaging the discounted payoff.

This project implements that pipeline for European calls and studies its numerical behavior:

* Geometric Brownian Motion
* Monte Carlo option pricing
* Historical volatility estimation
* Black-Scholes pricing
* Antithetic Variates
* Convergence analysis
* Simulation error

## Mathematical Framework

### Asset Price Simulation

The underlying asset is modeled with Geometric Brownian Motion:

```math
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t
```

Because GBM has an exact solution, the engine samples the terminal price directly under the risk-neutral measure, with no time-stepping:

```math
S_T = S_0 \exp\left[\left(r - \frac{\sigma^2}{2}\right)T + \sigma\sqrt{T}\,Z\right]
```

where:

* $`S_0`$ = current stock price
* $`r`$ = risk-free interest rate
* $`\sigma`$ = volatility
* $`T`$ = time to maturity
* $`Z \sim N(0,1)`$

### European Call Payoff

For a European call option:

```math
C_T = \max(S_T - K, 0)
```

The Monte Carlo estimate is:

```math
C_0 = e^{-rT}\,\frac{1}{N}\sum_{i=1}^{N}\max\left(S_T^{(i)} - K,\, 0\right)
```

where $`N`$ is the number of simulated terminal prices.

## Black-Scholes Benchmark

Simulated prices are evaluated against the analytical Black-Scholes price:

```math
C = S_0\,N(d_1) - K e^{-rT} N(d_2)
```

where:

```math
d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}
```

The closed-form result is the benchmark for judging Monte Carlo accuracy.

## Variance Reduction

### Antithetic Variates

For each random draw $`Z_i`$, the engine also uses its mirror $`-Z_i`$, and averages the two payoffs:

```math
\hat{C}_{anti} = e^{-rT}\,\frac{1}{N}\sum_{i=1}^{N}\frac{f(Z_i) + f(-Z_i)}{2}
```

Because the paired payoffs are negatively correlated, their average has lower variance than two independent draws.

### How the comparison is made

* The standard estimator uses `2N` independent draws.
* The antithetic estimator uses `N` pairs, which is also `2N` payoff evaluations.
* Standard error is the sample standard deviation divided by the square root of the number of independent samples (`2N` for standard, `N` pairs for antithetic).
* Variance reduction is reported as:

```math
1 - \left(\frac{SE_{anti}}{SE_{standard}}\right)^2
```

## Convergence Analysis

The convergence study compares each estimate with the Black-Scholes price as the number of simulations increases from 100 to 10,000 (40 log-spaced points), repeated for five historical volatility windows (30, 60, 90, 180 and 252 trading days).

For each simulation size the error is:

```math
\text{Error} = \left|\hat{C}_{MC} - C_{BS}\right|
```

This allows a direct comparison between standard Monte Carlo and Monte Carlo with Antithetic Variates.

## Volatility Estimation

Historical SPY prices are retrieved with the `yfinance` API. Returns are computed and annualized to estimate volatility over several observation windows, which shows how the choice of window changes the resulting option price and convergence behavior.

## Key Outputs

For each volatility window the program reports:

* Estimated annualized volatility
* Black-Scholes benchmark price
* Standard and antithetic Monte Carlo prices
* Absolute pricing error for each estimator
* Standard error for each estimator
* Convergence plots for standard vs. antithetic Monte Carlo

## Tech Stack

* Python
* NumPy
* SciPy
* Pandas
* Matplotlib
* yfinance
* Streamlit (interactive demo)

## Project Structure

```text
option-pricing-monte-carlo/
│
├── data/
│   └── fetch_data.py        # historical prices and annualized volatility
│
├── models/
│   ├── black_scholes.py     # closed-form benchmark
│   └── monte_carlo.py       # standard and antithetic Monte Carlo pricers
│
├── utils/
│   └── plotting.py          # convergence plots
│
├── app.py                   # Streamlit demo
├── main.py                  # command-line pricing run
├── montecarlo.ipynb         # notebook
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/rishi-bh/option-pricing-monte-carlo.git
cd option-pricing-monte-carlo
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the pricing engine from the command line:

```bash
python main.py
```

The program downloads SPY data, estimates volatility for each window, prices an at-the-money call with both estimators, compares the results with Black-Scholes, and plots convergence.

Run the interactive app locally:

```bash
streamlit run app.py
```

## Results & Analysis

The goal is not just to obtain an option price, but to study the numerical behavior of Monte Carlo estimation:

1. Simulation error shrinks as the number of simulations grows, but the standard estimator's error is noisy at small sample sizes.
2. Antithetic Variates reduced variance by 55.6% in the example run above, with a visibly tighter convergence curve around the Black-Scholes price.
3. The volatility window changes the input volatility and therefore the option price, which the program reports for each window.
4. Both estimators land within a fraction of a percent of the Black-Scholes price at 100,000 simulations.

## Limitations

The model relies on several simplifying assumptions:

* The underlying follows Geometric Brownian Motion.
* Volatility is estimated from historical data.
* The risk-free rate is assumed constant.
* European exercise is assumed.
* Transaction costs and market frictions are ignored.
* Black-Scholes assumptions do not perfectly describe real markets.
* Reported numbers come from a single unseeded run and will vary slightly between runs.

Consequently, this project is a study of numerical option pricing and Monte Carlo methods rather than a production trading system.

## Future Improvements

* Confidence intervals from the reported standard errors
* Fixed random seeds and averaging over repeated runs
* Control Variates
* Importance Sampling
* Quasi-Monte Carlo methods
* Stochastic volatility models
* American option pricing
* Greeks estimation
* Parallelized simulation
* GPU acceleration
* Out-of-sample volatility forecasting
