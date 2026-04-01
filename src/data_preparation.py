import pandas as pd

# 1. Load the dataset
# Make sure this file exists in your 'data' folder
df = pd.read_csv('data/Battery_Data_Cleaned.csv')

# --- FIX: Changed 'capacity' to 'Capacity' (Capital C) ---
# This matches your dataset columns: ['type', 'ambient_temperature', ..., 'Capacity']
max_cap = df['Capacity'].max()
df['SoH_Percentage'] = (df['Capacity'] / max_cap) * 100

# --- FIX: Placeholder for driving style ---
def categorize_driving(val):
    return 'Smooth'

df['driving_style'] = df['Capacity'].apply(categorize_driving)

# 2. Save the new prepared file for the AI Team
df.to_csv('data/Prepared_EV_Data.csv', index=False)

print("✅ Data Preparation Complete!")
print("📊 New column 'SoH_Percentage' created successfully.")