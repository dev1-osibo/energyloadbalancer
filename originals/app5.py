# app.py
import streamlit as st
import data_loader  # For loading CSV or HDF5 files
import baseline_calculator  # For calculating baseline metrics
import simulator  # For running the optimization simulation
import matplotlib.pyplot as plt

# Set the page configuration
st.set_page_config(page_title="Data Center Energy Optimization", layout="wide")

# Title and Description
st.title("Data Center Energy Optimization Simulator")
st.write("""
This app simulates the impact of shifting data center workloads to periods of higher renewable energy availability. 
Additionally, it provides forecasts for future energy consumption and cost savings.
""")

# Sidebar Inputs: File Uploader (supports both .csv and .h5)
uploaded_file = st.sidebar.file_uploader("Upload your data file", type=["csv", "h5"])

# Load data based on file type
if uploaded_file:
    file_type = "csv" if uploaded_file.name.endswith('.csv') else "h5"
    data = data_loader.load_data(uploaded_file, file_type)
else:
    st.sidebar.write("Using default synthetic dataset.")
    data = data_loader.load_data('synthetic_data_center_data.csv', file_type="csv")

# Display loaded data preview
st.write("Loaded Data Preview:", data.head())

# Sidebar sliders for adjustable parameters
energy_price_per_kwh = st.sidebar.slider("Energy Price per kWh ($)", min_value=0.05, max_value=1.00, value=0.1, step=0.01)
emission_factor_non_renewable = st.sidebar.slider("Emission Factor for Non-Renewable (kg CO₂ per kWh)", min_value=0.1, max_value=1.0, value=0.5, step=0.05)
emission_factor_renewable = st.sidebar.slider("Emission Factor for Renewable (kg CO₂ per kWh)", min_value=0.0, max_value=0.5, value=0.02, step=0.01)
renewable_threshold = st.sidebar.slider("Renewable Energy Availability Threshold (%)", min_value=0, max_value=100, value=70, step=5) / 100

# New slider for baseline load factor
baseline_load_factor = st.sidebar.slider("Baseline Load Factor", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# Apply the baseline load factor to adjust the workload energy consumption
data['Adjusted Workload Energy Consumption (kWh)'] = data['Workload Energy Consumption (kWh)'] * baseline_load_factor

# Calculate and display baseline metrics with adjusted load
baseline_results = baseline_calculator.calculate_baseline(data, energy_price_per_kwh, emission_factor_non_renewable)
st.header("Baseline Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Energy Consumption (kWh)", f"{baseline_results['total_energy']:.2f}")
col2.metric("Total Cost ($)", f"{baseline_results['total_cost']:.2f}")
col3.metric("Total CO₂ Emissions (kg)", f"{baseline_results['total_emissions']:.2f}")

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

        # Display optimized results side by side in a consistent layout
        st.header("Optimized Metrics")
        col1, col2, col3 = st.columns(3)

        # Energy Savings
        energy_savings = simulation_results['energy_savings']
        energy_color = "normal" if energy_savings > 0 else "inverse"
        energy_arrow = "⬇️" if energy_savings > 0 else "⬆️"
        col1.metric(
            "Optimized Energy Consumption (kWh)", 
            f"{simulation_results['optimized_energy']:.2f}", 
            delta=f"{energy_arrow} {abs(energy_savings):.2f} kWh saved" if energy_savings > 0 else f"{energy_arrow} {abs(energy_savings):.2f} kWh increased",
            delta_color=energy_color
        )

        # Cost Savings
        cost_savings = simulation_results['cost_savings']
        cost_color = "normal" if cost_savings > 0 else "inverse"
        cost_arrow = "⬇️" if cost_savings > 0 else "⬆️"
        col2.metric(
            "Optimized Cost ($)", 
            f"{simulation_results['optimized_cost']:.2f}", 
            delta=f"{cost_arrow} ${abs(cost_savings):.2f} saved" if cost_savings > 0 else f"{cost_arrow} ${abs(cost_savings):.2f} increased",
            delta_color=cost_color
        )

        # Emissions Savings
        emissions_savings = simulation_results['emissions_savings']
        emissions_color = "normal" if emissions_savings > 0 else "inverse"
        emissions_arrow = "⬇️" if emissions_savings > 0 else "⬆️"
        col3.metric(
            "Optimized CO₂ Emissions (kg)", 
            f"{simulation_results['optimized_emissions']:.2f}", 
            delta=f"{emissions_arrow} {abs(emissions_savings):.2f} kg CO₂ reduced" if emissions_savings > 0 else f"{emissions_arrow} {abs(emissions_savings):.2f} kg CO₂ increased",
            delta_color=emissions_color
        )

        # Display charts comparing baseline and optimized metrics
        st.subheader("Energy Comparison")
        st.write("This chart compares baseline vs. optimized energy consumption over time.")
        data['Optimized Energy (kWh)'] = simulation_results['optimized_energy']
        st.line_chart(data[['Adjusted Workload Energy Consumption (kWh)', 'Optimized Energy (kWh)']])
