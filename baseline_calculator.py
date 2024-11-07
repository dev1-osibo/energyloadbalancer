# baseline_calculator.py

import pandas as pd

def calculate_baseline(data, energy_price_per_kwh=0.1, emission_factor_non_renewable=0.5):
    """
    Calculate the baseline energy consumption, cost, and CO? emissions.

    Parameters:
    - data: DataFrame, contains workload energy consumption data (kWh).
    - energy_price_per_kwh: float, cost per kWh of energy (default is $0.1).
    - emission_factor_non_renewable: float, CO? emissions factor per kWh (kg CO? per kWh, default is 0.5).

    Assumes that the DataFrame 'data' has a column 'Workload Energy Consumption (kWh)'.

    Returns:
    - Dictionary with baseline metrics: total energy, total cost, total emissions.
    """
   
# Ensure the column is numeric
    data['Workload Energy Consumption (kWh)'] = pd.to_numeric(data['Workload Energy Consumption (kWh)'], errors='coerce')

 # Check if the expected column exists in the data
    if 'Workload Energy Consumption (kWh)' not in data.columns:
        raise ValueError("Data must contain a 'Workload Energy Consumption (kWh)' column.")

    # Calculate total energy consumption
    total_energy = data['Workload Energy Consumption (kWh)'].sum()

    # Calculate total cost
    total_cost = total_energy * energy_price_per_kwh

    # Calculate total emissions (assuming all energy is non-renewable for baseline)
    total_emissions = total_energy * emission_factor_non_renewable

    # Return the calculated baseline metrics
    return {
        'total_energy': total_energy,
        'total_cost': total_cost,
        'total_emissions': total_emissions
    }