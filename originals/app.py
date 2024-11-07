# app.py
import data_loader #For loading CSV or HDF5 files
import baseline_calculator # For calculating baseline metrics
import streamlit as st
import pandas as pd
import simulator # For running the optimization simulation
import matplotlib.pyplot as plt
import energy_simulation  # Import your custom module

# Set the page configuration
st.set_page_config(page_title="Data Center Energy Optimization", layout="wide")

# Title and Description
st.title("Data Center Energy Optimization Simulator")
st.write("""
This app simulates the impact of shifting data center workloads to periods of higher renewable energy availability. 
Additionally, it provides forecasts for future energy consumption and cost savings.
""")

# Sidebar Inputs: File Uploader (supports both .csv and .h5)
uploaded_file = st.sidebar.file_uploader("Upload your CSV data file", type=["csv", "h5"])

# Load data based on file type
if uploaded_file:
    file_type = "csv" if uploaded_file.name.endswith('.csv') else "h5"
    data = data_loader.load_data(uploaded_file, file_type)
else:
    st.sidebar.write("Using default synthetic dataset.")
    # Assuming you have a default CSV or synthetic data loader
    data = data_loader.load_data('synthetic_data_center_data.csv', file_type="csv")

# Display loaded data preview
st.write("Loaded Data Preview:", data.head())

# Sidebar sliders for adjustable parameters
energy_price_per_kwh = st.sidebar.slider("Energy Price per kWh ($)", min_value=0.05, max_value=1.00, value=0.1, step=0.01)
emission_factor_non_renewable = st.sidebar.slider("Emission Factor for Non-Renewable (kg CO? per kWh)", min_value=0.1, max_value=1.0, value=0.5, step=0.05)
emission_factor_renewable = st.sidebar.slider("Emission Factor for Renewable (kg CO? per kWh)", min_value=0.0, max_value=0.5, value=0.02, step=0.01)

# Sidebar sliders for adjustable parameters
#energy_price_per_kwh = st.sidebar.slider("Energy Price per kWh #($)", min_value=0.05, max_value=1.00, value=0.1, step=0.01)
#emission_factor_non_renewable = st.sidebar.slider("Emission #Factor (kg CO? per kWh)", min_value=0.1, max_value=1.0, value=0.5, step=0.05)

# Calculate and display baseline metrics using adjustable values from sliders
baseline_results = baseline_calculator.calculate_baseline(data, energy_price_per_kwh, emission_factor_non_renewable)

# Display Baseline Metrics
st.header("Baseline Metrics")
st.metric("Total Energy Consumption (kWh)", f"{baseline_results['total_energy']:.2f}")
st.metric("Total Cost ($)", f"{baseline_results['total_cost']:.2f}")
st.metric("Total CO? Emissions (kg)", f"{baseline_results['total_emissions']:.2f}")

# Run the simulation and display optimized metrics
if st.sidebar.button('Run Simulation'):
    with st.spinner('Running simulation...'):
        simulation_results = simulator.run_simulation(
            data, 
            renewable_threshold, 
            energy_price_per_kwh, 
            emission_factor_non_renewable, 
            emission_factor_renewable
        )

# Display optimized results
    st.header("Optimized Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Optimized Energy Consumption (kWh)", f"{simulation_results['optimized_energy']:.2f}", delta=f"{simulation_results['energy_savings']:.2f} kWh saved")
    col2.metric("Optimized Cost ($)", f"{simulation_results['optimized_cost']:.2f}", delta=f"${simulation_results['cost_savings']:.2f} saved")
    col3.metric("Optimized CO? Emissions (kg)", f"{simulation_results['optimized_emissions']:.2f}", delta=f"{simulation_results['emissions_savings']:.2f} kg CO? reduced")

# Display charts comparing baseline and optimized metrics
    st.subheader("Energy Comparison")
    st.write("This chart compares baseline vs. optimized energy consumption over time.")
    data['Optimized Energy (kWh)'] = simulation_results['optimized_energy']
    st.line_chart(data[['Workload Energy Consumption (kWh)', 'Optimized Energy (kWh)']])

# Sidebar Inputs: Renewable Threshold Slider
#renewable_threshold = st.sidebar.slider(
    #'Renewable Energy Availability Threshold (%)',
    #min_value=0, max_value=100, value=70, step=5
#) / 100  # Convert to fraction

# Run Simulation Button
if st.sidebar.button('Run Simulation'):
    with st.spinner('Running simulation...'):
        results = energy_simulation.run_simulation(data, renewable_threshold)

    if results:
        # Display Simulation Results
        st.header("Simulation Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Baseline Energy (kWh)", f"{results['total_baseline_energy']:.2f}")
        col2.metric("Optimized Energy (kWh)", f"{results['total_optimized_energy']:.2f}")
        col3.metric("Energy Savings (kWh)", f"{results['energy_savings']:.2f}")

        # Plot Energy Consumption Over Time
        df = results['df']
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['Timestamp'], df['Baseline Energy (kWh)'], label='Baseline Energy')
        ax.plot(df['Timestamp'], df['Optimized Energy (kWh)'], label='Optimized Energy')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Energy Consumption (kWh)')
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Simulation failed. Please check the input data.")

# Run Simulation and Forecast Button (INSERT THIS SECTION HERE)
if st.sidebar.button('Run Simulation and Forecast'):
    with st.spinner('Running simulation and forecasting...'):
        # Step 1: Run the simulation to get optimized energy consumption
        results = energy_simulation.run_simulation(data, renewable_threshold)

        if results:
            # Step 2: Use optimized energy data for forecasting
            forecast_data = results['df'][['Timestamp', 'Optimized Energy (kWh)']]
            forecast_data = forecast_data.rename(columns={'Timestamp': 'ds', 'Optimized Energy (kWh)': 'y'})

            # Step 3: Forecast future energy consumption based on optimized data
            forecast = energy_simulation.forecast_energy(forecast_data, periods=24)

            # Step 4: Display Simulation and Forecast Results
            st.header("Simulation Results with Forecasting")

            # Display Metrics: Energy, Cost, and Emissions Savings
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Baseline Energy (kWh)", f"{results['total_baseline_energy']:.2f}")
            col1.metric("Total Optimized Energy (kWh)", f"{results['total_optimized_energy']:.2f}")
            col1.metric("Energy Savings (kWh)", f"{results['energy_savings']:.2f}",
                        delta=f"{(results['energy_savings'] / results['total_baseline_energy']) * 100:.2f}%")

            col2.metric("Baseline Cost ($)", f"{results['total_baseline_cost']:.2f}")
            col2.metric("Optimized Cost ($)", f"{results['total_optimized_cost']:.2f}")
            col2.metric("Cost Savings ($)", f"{results['cost_savings']:.2f}",
                        delta=f"{(results['cost_savings'] / results['total_baseline_cost']) * 100:.2f}%")

            col3.metric("Baseline Emissions (kg CO?)", f"{results['total_baseline_emissions']:.2f}")
            col3.metric("Optimized Emissions (kg CO?)", f"{results['total_optimized_emissions']:.2f}")
            col3.metric("Emissions Reduction (kg CO?)", f"{results['emissions_reduction']:.2f}",
                        delta=f"{results['carbon_footprint_impact']:.2f}%")

            # Step 5: Visualize Forecasted Energy Consumption
            st.subheader("Forecasted Optimized Energy Consumption")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(forecast['ds'], forecast['yhat'], label='Forecasted Optimized Energy (kWh)')
            ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], 
                            color='gray', alpha=0.2, label='Confidence Interval')
            ax.set_xlabel('Time')
            ax.set_ylabel('Energy Consumption (kWh)')
            ax.set_title('Forecasted Optimized Energy Consumption')
            ax.legend()
            st.pyplot(fig)
        else:
            st.error("Simulation failed. Please check the input data.")