# energy_simulation.py
# © 2024 Babasola Osibo. All Rights Reserved.

import numpy as np
import pandas as pd
from prophet import Prophet  # Import Prophet for forecasting

def load_data(file_path):
    """
    Loads the dataset from the specified CSV file.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded dataset.
    """
    data = pd.read_csv(file_path)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    return data

def run_simulation(data, renewable_threshold=0.70, emission_factor_non_renewable=0.5, emission_factor_renewable=0.02):
    """
    Runs the energy optimization simulation.

    Parameters:
        data (pandas.DataFrame): The input dataset.
        renewable_threshold (float): The threshold for renewable energy availability (between 0 and 1).
        emission_factor_non_renewable (float): Emission factor for non-renewable energy (kg CO2 per kWh).
        emission_factor_renewable (float): Emission factor for renewable energy (kg CO2 per kWh).

    Returns:
        dict: A dictionary containing simulation results and data for visualization.
    """
    # Extract variables from the dataset
    timestamps = data['Timestamp']
    energy_prices = data['Energy Price ($/kWh)'].values
    renewable_availability = data['Renewable Availability (%)'].values / 100  # Convert to fraction
    workload_energy = data['Workload Energy Consumption (kWh)'].values

    # Step 2: Calculate Baseline Metrics
    baseline_energy_consumption = workload_energy.copy()
    baseline_cost = baseline_energy_consumption * energy_prices
    baseline_renewable_energy = baseline_energy_consumption * renewable_availability
    baseline_non_renewable_energy = baseline_energy_consumption - baseline_renewable_energy
    baseline_emissions = (
        baseline_non_renewable_energy * emission_factor_non_renewable +
        baseline_renewable_energy * emission_factor_renewable
    )

    # Step 3: Optimize Workload Schedule
    optimal_hours = renewable_availability >= renewable_threshold
    optimized_workload_energy = workload_energy.copy()

    # Calculate total energy to shift
    energy_to_shift = np.sum(
        workload_energy[~optimal_hours] * (renewable_threshold - renewable_availability[~optimal_hours])
    )

    # Increase workload during optimal hours
    for i in range(len(timestamps)):
        if optimal_hours[i]:
            max_additional_energy = workload_energy[i] * 0.2  # Allow up to 20% increase
            shift_amount = min(energy_to_shift, max_additional_energy)
            optimized_workload_energy[i] += shift_amount
            energy_to_shift -= shift_amount
            if energy_to_shift <= 0:
                break

    # Decrease workload during non-optimal hours
    for i in range(len(timestamps)):
        if not optimal_hours[i]:
            reduction = workload_energy[i] * 0.1  # Reduce by 10%
            optimized_workload_energy[i] -= reduction

    # Ensure no negative workloads
    optimized_workload_energy = np.maximum(optimized_workload_energy, 0)

    # Step 4: Calculate Optimized Metrics
    optimized_energy_consumption = optimized_workload_energy
    optimized_cost = optimized_energy_consumption * energy_prices
    optimized_renewable_energy = optimized_energy_consumption * renewable_availability
    optimized_non_renewable_energy = optimized_energy_consumption - optimized_renewable_energy
    optimized_emissions = (
        optimized_non_renewable_energy * emission_factor_non_renewable +
        optimized_renewable_energy * emission_factor_renewable
    )

    # Step 5: Compare Results
    total_baseline_energy = np.sum(baseline_energy_consumption)
    total_optimized_energy = np.sum(optimized_energy_consumption)
    energy_savings = total_baseline_energy - total_optimized_energy

    total_baseline_cost = np.sum(baseline_cost)
    total_optimized_cost = np.sum(optimized_cost)
    cost_savings = total_baseline_cost - total_optimized_cost

    total_baseline_emissions = np.sum(baseline_emissions)
    total_optimized_emissions = np.sum(optimized_emissions)
    emissions_reduction = total_baseline_emissions - total_optimized_emissions

    # Carbon footprint impact (percentage reduction)
    carbon_footprint_impact = (emissions_reduction / total_baseline_emissions) * 100 if total_baseline_emissions != 0 else 0

    # Prepare results
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'Baseline Energy (kWh)': baseline_energy_consumption,
        'Optimized Energy (kWh)': optimized_energy_consumption,
        'Renewable Availability (%)': renewable_availability * 100,
        'Energy Price ($/kWh)': energy_prices
    })

    results = {
        'total_baseline_energy': total_baseline_energy,
        'total_optimized_energy': total_optimized_energy,
        'energy_savings': energy_savings,
        'total_baseline_cost': total_baseline_cost,
        'total_optimized_cost': total_optimized_cost,
        'cost_savings': cost_savings,
        'total_baseline_emissions': total_baseline_emissions,
        'total_optimized_emissions': total_optimized_emissions,
        'emissions_reduction': emissions_reduction,
        'carbon_footprint_impact': carbon_footprint_impact,
        'df': df  # DataFrame for visualization
    }

    return results  # Ensure the return is properly aligned with function

# Place the forecast_energy() function here at the bottom of the file
def forecast_energy(data, periods=24):
    """
    Forecast future energy consumption or renewable availability using Prophet.

    Parameters:
        data (pandas.DataFrame): The input dataset with timestamps and values to forecast.
        periods (int): Number of future periods to forecast (e.g., 24 hours).

    Returns:
        pandas.DataFrame: Forecasted data with predictions.
    """
    # Prepare the data for Prophet
    df = data.rename(columns={'Timestamp': 'ds', data.columns[1]: 'y'})  # Rename for Prophet

    # Initialize and fit the model
    model = Prophet()
    model.fit(df)

    # Create a future dataframe for predictions
    future = model.make_future_dataframe(periods=periods, freq='H')  # Forecast hourly for 24 periods
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]  # Return relevant forecast data