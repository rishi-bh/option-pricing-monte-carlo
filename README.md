# Monte Carlo Option Pricing Engine

A Python-based Monte Carlo simulation engine for pricing European call options using historical volatility estimates. The project compares simulated option prices against the Black-Scholes analytical solution and investigates the effect of Antithetic Variates on Monte Carlo convergence.

## Overview

Monte Carlo methods provide a flexible approach to derivative pricing by simulating possible future asset-price paths and estimating the expected discounted payoff.

This project implements a Monte Carlo pricing framework for European call options and evaluates how quickly the simulation converges toward the Black-Scholes theoretical price.

The project focuses on:

* Geometric Brownian Motion
* Monte Carlo option pricing
* Historical volatility estimation
* Black-Scholes pricing
* Antithetic Variates
* Convergence analysis
* Simulation error

## Mathematical Framework

### Asset Price Simulation

The underlying asset is modeled using Geometric Brownian Motion:

$
dS_t = \mu S_tdt+\sigma S_tdW_t
$

Under the risk-neutral measure, the simulated terminal price is:

$
S_T =
S_0
\exp\left[
\left(r-\frac{\sigma^2}{2}\right)T
+\sigma\sqrt{T}Z
\right]
$

where:

* $S_0$ = current stock price
* $r$ = risk-free interest rate
* $\sigma$ = volatility
* $T$ = time to maturity
* $Z\sim N(0,1)$

### European Call Payoff

For a European call option:

$
C_T=\max(S_T-K,0)
$

The Monte Carlo estimate is:

$
C_0 =
e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
\max(S_T^{(i)}-K,0)
$

where (N) is the number of simulated paths.

## Black-Scholes Benchmark

The simulation is evaluated against the analytical Black-Scholes price:

$
C =
S_0N(d_1)-Ke^{-rT}N(d_2)
$

where:

$
d_1=
\frac{\ln(S_0/K)+(r+\sigma^2/2)T}
{\sigma\sqrt{T}}
$

and

$
d_2=d_1-\sigma\sqrt{T}
$

The Black-Scholes result provides a theoretical benchmark for evaluating Monte Carlo convergence.

## Variance Reduction

### Antithetic Variates

The project implements Antithetic Variates to reduce Monte Carlo estimator variance.

For each simulated random variable (Z), a corresponding (-Z) is generated:

$
Z_i,\quad -Z_i
$

The resulting terminal prices are used to construct paired payoff estimates.

The estimator becomes:

$
\hat{C} =
e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
\frac{f(Z_i)+f(-Z_i)}{2}
$

Because the paired simulations are negatively correlated, this can reduce estimator variance without requiring additional independent random draws.

## Convergence Analysis

The model evaluates convergence by comparing the Monte Carlo estimate against the Black-Scholes benchmark as the number of simulations increases.

For each simulation size, the model can measure:

$
Error = |\hat{C}*{MC}-C*{BS}|
$

This allows comparison between:

* Standard Monte Carlo
* Monte Carlo with Antithetic Variates

The expected result is faster convergence and lower estimation error when variance reduction is effective.

## Volatility Estimation

Historical stock-price data is retrieved using the `yfinance` API.

Historical returns are calculated and used to estimate volatility over different observation windows.

This allows the model to investigate how the choice of historical volatility window affects the resulting option price and convergence behavior.

## Key Outputs

The model produces:

* Monte Carlo option price
* Black-Scholes benchmark price
* Absolute pricing error
* Estimated volatility
* Convergence behavior
* Comparison between standard and variance-reduced Monte Carlo

Example:

```text
Monte Carlo Price:      $X.XXXX
Black-Scholes Price:    $X.XXXX
Absolute Error:         $X.XXXX
```

## Tech Stack

* Python
* NumPy
* Pandas
* Matplotlib
* yfinance

## Project Structure

```text
monte-carlo-option-pricing/
│
├── data/
│   └── fetch_data.py
│
├── models/
│   ├── black_scholes.py
│   └── monte_carlo.py
│
├── utils/
│   └── plotting.py
│
├── main.py
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd monte-carlo-option-pricing
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install numpy pandas matplotlib yfinance
```

## Usage

Run the pricing engine:

```bash
python option_pricing.py
```

The program retrieves historical market data, estimates volatility, simulates option prices, and compares the results with the Black-Scholes analytical solution.

## Results & Analysis

The primary objective is not simply to obtain an option price, but to study the numerical behavior of Monte Carlo estimation.

The analysis examines:

1. How simulation error decreases as the number of paths increases.
2. How Antithetic Variates affect estimator variance.
3. How different historical volatility windows affect option prices.
4. How closely the simulation approaches the Black-Scholes benchmark.

## Limitations

The model relies on several simplifying assumptions:

* The underlying follows Geometric Brownian Motion.
* Volatility is estimated from historical data.
* The risk-free rate is assumed constant.
* European exercise is assumed.
* Transaction costs and market frictions are ignored.
* Black-Scholes assumptions do not perfectly describe real markets.

Consequently, the project is primarily a study of numerical option pricing and Monte Carlo methods rather than a production trading system.

## Future Improvements

Potential extensions include:

* Confidence intervals for Monte Carlo estimates
* Control Variates
* Importance Sampling
* Quasi-Monte Carlo methods
* Stochastic volatility models
* American option pricing
* Greeks estimation
* Parallelized simulation
* GPU acceleration
* Out-of-sample volatility forecasting
