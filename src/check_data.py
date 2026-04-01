import pandas as pd

# This tells Python to look inside the data folder for your file
# IMPORTANT: Change 'battery_data.csv' to the EXACT name of your file
file_path = 'data/Battery_Data_Cleaned.csv' 

try:
    df = pd.read_csv(file_path)
    print("✅ Success! Data loaded.")
    print("\n--- First 5 rows of sensor data ---")
    print(df.head())
    print("\n--- Columns found (Voltage, Temp, etc.) ---")
    print(df.columns)
except Exception as e:
    print(f"❌ Error: {e}")