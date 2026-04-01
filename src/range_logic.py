import pickle
import pandas as pd

# 1. Load the AI "Brain" (Created by Members 3 & 4)
with open('models/battery_model.pkl', 'rb') as f:
    model = pickle.load(f)

def estimate_ev_range(resistance, temp, style):
    # Prepare the input for the AI
    # We use 'Re', 'Rct', 'ambient_temperature', and a dummy 'test_id'
    input_data = pd.DataFrame([[resistance, 0.1, temp, 1]], 
                               columns=['Re', 'Rct', 'ambient_temperature', 'test_id'])
    
    # Step A: Get the AI's Health Prediction (SoH %)
    predicted_soh = model.predict(input_data)[0]
    
    # Step B: Base Range Calculation (Assume 200km is 100% Health)
    base_km = (predicted_soh / 100) * 200
    
    # Step C: Real-World Adjustments (Member 5's Logic)
    if temp > 40:
        base_km *= 0.85  # 15% reduction for extreme heat
    
    if style == "Aggressive":
        base_km *= 0.75  # 25% reduction for fast driving
        
    return round(predicted_soh, 2), round(base_km, 2)

# --- TEST THE LOGIC ---
if __name__ == "__main__":
    health, km = estimate_ev_range(0.08, 42, "Aggressive")
    print(f"🔋 AI Predicted Health: {health}%")
    print(f"🚗 Estimated Driving Range: {km} km")