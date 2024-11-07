# data_loader.py
import pandas as pd
import numpy as np
import h5py

def load_data(file_path, file_type="csv", dataset_name="cf"):
    """
    Load data from a CSV or HDF5 (.h5) file and return a DataFrame with timestamps.

    Parameters:
    - file_path: str, path to the file.
    - file_type: str, "csv" or "h5", indicating the file type.
    - dataset_name: str, name of the dataset within the .h5 file (default is 'cf').
- start_date: str, start date for generated timestamps in .h5 files (default is "2023-01-01").
    - freq: str, frequency of generated timestamps in .h5 files (default is "H" for hourly).
    Returns:
    - DataFrame with data and timestamps.
    """
    if file_type == "csv":
        data = pd.read_csv(file_path)

  # Try to parse different timestamp formats
        try:
            # Try parsing yyyymm format
            data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y%m')
        except ValueError:
            # If it fails, try standard datetime format
            data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        
        data.set_index('Timestamp', inplace=True)

        # Convert `yyyymm` format to a proper datetime format
        #data['Timestamp'] = pd.to_datetime(data['Timestamp'], #format='%Y%m')
        #data.set_index('Timestamp', inplace=True)

        #data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        #data.set_index('Timestamp', inplace=True)

    elif file_type == "h5":
        with h5py.File(file_path, 'r') as f:
            data = f[dataset_name][:]
            data = pd.DataFrame(data)
            # Assuming data is hourly; adjust start date as needed
            data['Timestamp'] = pd.date_range(start='2023-01-01', periods=len(data), freq='H')
            data.set_index('Timestamp', inplace=True)
    else:
        raise ValueError("Unsupported file type. Use 'csv' or 'h5'.")

  # Check if 'Renewable Availability (%)' column exists; add synthetic values if missing
    if 'Renewable Availability (%)' not in data.columns:
        data['Renewable Availability (%)'] = np.where(
            (data.index.hour >= 6) & (data.index.hour <= 18),
            np.random.uniform(60, 100, len(data)),  # Higher availability during the day
            np.random.uniform(0, 40, len(data))      # Lower availability at night
        )

    return data