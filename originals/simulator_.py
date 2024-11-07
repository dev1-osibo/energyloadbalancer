import numpy as np
import pandas as pd

def run_simulation(data, renewable_threshold, energy_price_per_kwh, emission_factor_non_renewable, emission_factor_renewable):
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
        'optimized_energy': data['Optimized Energy'].sum(),
        'optimized_cost': (data['Optimized Energy'] * energy_price_per_kwh).sum(),
        'optimized_emissions': data['Optimized Emissions'].sum(),
        'energy_savings': data['Workload Energy Consumption (kWh)'].sum() - data['Optimized Energy'].sum(),
        'cost_savings': (data['Workload Energy Consumption (kWh)'] * energy_price_per_kwh).sum() - (data['Optimized Energy'] * energy_price_per_kwh).sum(),
        'emissions_savings': data['Baseline Emissions'].sum() - data['Optimized Emissions'].sum(),
    }
    return results
