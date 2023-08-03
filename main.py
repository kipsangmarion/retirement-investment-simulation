import numpy as np


# Function to simulate retirement journey and calculate fund balance
def retirement_simulation(initial_balance, monthly_contribution, retirement_expenses,
                          retirement_duration, investment_returns, inflation_rates,
                          lifespan, tax_rate, social_security_benefit):
    num_months = retirement_duration * 12
    balance = initial_balance
    social_security_months = 12 * (lifespan - retirement_duration)

    for month in range(num_months):
        # Adjust contributions and expenses for inflation
        real_monthly_contribution = monthly_contribution * (1 + inflation_rates[month] / 12)
        real_retirement_expenses = retirement_expenses * (1 + inflation_rates[month] / 12)

        # Calculate investment return for the month
        investment_return = np.random.normal(investment_returns[month] / 12, investment_returns.std() / np.sqrt(12))

        # Apply taxes on investment returns
        after_tax_return = investment_return * (1 - tax_rate)

        # Update balance for the month
        balance = balance * (1 + after_tax_return) + real_monthly_contribution - real_retirement_expenses

        # Consider Social Security benefits
        if month >= social_security_months:
            balance += social_security_benefit / 12

        # Check if the individual outlives their retirement duration
        if month >= lifespan * 12:
            break

    return balance


# Main Monte Carlo simulation function
def monte_carlo_retirement_simulation(num_simulations, initial_balance, monthly_contribution,
                                      retirement_expenses, retirement_duration,
                                      investment_returns_mean, investment_returns_volatility,
                                      inflation_rate_mean, inflation_rate_volatility,
                                      lifespan, tax_rate, social_security_benefit):
    results = []

    for _ in range(num_simulations):
        # Generate random investment returns and inflation rates for each month
        investment_returns = np.random.normal(investment_returns_mean, investment_returns_volatility, retirement_duration * 12)
        inflation_rates = np.random.normal(inflation_rate_mean, inflation_rate_volatility, retirement_duration * 12)

        balance = retirement_simulation(initial_balance, monthly_contribution, retirement_expenses,
                                        retirement_duration, investment_returns, inflation_rates,
                                        lifespan, tax_rate, social_security_benefit)
        results.append(balance)

    return results


# Input parameters for the simulation
num_simulations = 10000
initial_balance = 500000
monthly_contribution = 3000
retirement_expenses = 4000
retirement_duration = 30
investment_returns_mean = 0.06
investment_returns_volatility = 0.12
inflation_rate_mean = 0.02
inflation_rate_volatility = 0.005
lifespan = 85
tax_rate = 0.15
social_security_benefit = 2000  # Monthly Social Security benefit

# Run the Monte Carlo simulation
simulation_results = monte_carlo_retirement_simulation(num_simulations, initial_balance, monthly_contribution,
                                                       retirement_expenses, retirement_duration,
                                                       investment_returns_mean, investment_returns_volatility,
                                                       inflation_rate_mean, inflation_rate_volatility,
                                                       lifespan, tax_rate, social_security_benefit)

# Calculate the probability of retirement savings lasting until the end of retirement
probability_success = sum(result >= 0 for result in simulation_results) / num_simulations

print(f"Probability of retirement savings lasting until the end of retirement: {probability_success:.2f}")
