# simulator.py

import pandas as pd
import numpy as np

def run_simulation(data, renewable_threshold, energy_price_per_kwh, emission_factor_non_renewable, emission_factor_renewable):
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
    # Step 1: Calculate baseline emissions
    data['Baseline Emissions'] = (
        data['Workload Energy Consumption (kWh)'] * emission_factor_non_renewable * 
        (1 - data['Renewable Availability (%)'] / 100) + 
        data['Workload Energy Consumption (kWh)'] * emission_factor_renewable * 
        (data['Renewable Availability (%)'] / 100)
    )

    # Step 2: Optimize by favoring renewable hours
    data['Optimized Energy'] = np.where(
        data['Renewable Availability (%)'] >= renewable_threshold * 100, 
        data['Workload Energy Consumption (kWh)'], 
        data['Workload Energy Consumption (kWh)'] * 0.9  # Reduce energy usage if renewables are unavailable
    )

    # Recalculate emissions after optimization
    data['Optimized Emissions'] = (
        data['Optimized Energy'] * emission_factor_non_renewable * 
        (1 - data['Renewable Availability (%)'] / 100) + 
        data['Optimized Energy'] * emission_factor_renewable * 
        (data['Renewable Availability (%)'] / 100)
    )

    # Calculate total values
    results = {
        'baseline_energy': data['Workload Energy Consumption (kWh)'].sum(),
        'optimized_energy': data['Optimized Energy'].sum(),
        'energy_savings': data['Workload Energy Consumption (kWh)'].sum() - data['Optimized Energy'].sum(),
        'baseline_cost': (data['Workload Energy Consumption (kWh)'] * energy_price_per_kwh).sum(),
        'optimized_cost': (data['Optimized Energy'] * energy_price_per_kwh).sum(),
        'cost_savings': (data['Workload Energy Consumption (kWh)'] * energy_price_per_kwh).sum() - (data['Optimized Energy'] * energy_price_per_kwh).sum(),
        'baseline_emissions': data['Baseline Emissions'].sum(),
        'optimized_emissions': data['Optimized Emissions'].sum(),
        'emissions_savings': data['Baseline Emissions'].sum() - data['Optimized Emissions'].sum(),
    }
    return results