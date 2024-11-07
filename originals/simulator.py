# simulator.py

import pandas as pd

def run_simulation(data, renewable_threshold=0.7, energy_price_per_kwh=0.1, emission_factor_non_renewable=0.5, emission_factor_renewable=0.02):
    """
    Simulate optimized energy, cost, and emissions by shifting workloads to align with renewable energy availability.

    Parameters:
    - data: DataFrame containing workload energy data (kWh) and renewable availability.
    - renewable_threshold: float, percentage threshold (0-1) for renewable energy availability to prioritize green energy.
    - energy_price_per_kwh: float, cost per kWh of energy.
    - emission_factor_non_renewable: float, CO? emissions factor for non-renewable energy (kg CO? per kWh).
    - emission_factor_renewable: float, CO? emissions factor for renewable energy (kg CO? per kWh).

    Returns:
    - Dictionary with optimized metrics: total energy, total cost, total emissions, energy savings, cost savings, emissions savings.
    """
    # Check if renewable availability is in the dataset
    if 'Renewable Availability (%)' not in data.columns:
        raise ValueError("Data must contain a 'Renewable Availability (%)' column.")

    # Convert renewable availability to a fraction
    data['Renewable Availability'] = data['Renewable Availability (%)'] / 100

    # Baseline calculations (without optimization)
    baseline_energy = data['Workload Energy Consumption (kWh)'].sum()
    baseline_cost = baseline_energy * energy_price_per_kwh
    baseline_emissions = baseline_energy * emission_factor_non_renewable

    # Optimized calculations (with workload shifting to green energy periods)
    data['Optimized Energy (kWh)'] = data.apply(
        lambda row: row['Workload Energy Consumption (kWh)'] * row['Renewable Availability']
        if row['Renewable Availability'] >= renewable_threshold else row['Workload Energy Consumption (kWh)'],
        axis=1
    )
    
    # Calculate optimized cost and emissions
    optimized_energy = data['Optimized Energy (kWh)'].sum()
    optimized_cost = optimized_energy * energy_price_per_kwh
    optimized_emissions = (
        (data['Optimized Energy (kWh)'] * emission_factor_renewable) + 
        ((baseline_energy - optimized_energy) * emission_factor_non_renewable)
    ).sum()

    # Calculate savings
    energy_savings = baseline_energy - optimized_energy
    cost_savings = baseline_cost - optimized_cost
    emissions_savings = baseline_emissions - optimized_emissions

    return {
        'baseline_energy': baseline_energy,
        'optimized_energy': optimized_energy,
        'energy_savings': energy_savings,
        'baseline_cost': baseline_cost,
        'optimized_cost': optimized_cost,
        'cost_savings': cost_savings,
        'baseline_emissions': baseline_emissions,
        'optimized_emissions': optimized_emissions,
        'emissions_savings': emissions_savings
    }