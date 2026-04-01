import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.range_logic import estimate_ev_range

# 1. Page Configuration
st.set_page_config(page_title="EV Battery Intelligence", layout="wide")

# 2. Sidebar Inputs
st.sidebar.header("🔌 Battery Parameters")
voltage = st.sidebar.slider("Voltage (V)", 2.0, 4.5, 3.7)
temp = st.sidebar.slider("Ambient Temperature (°C)", -10, 60, 25)
style = st.sidebar.selectbox("Driving Style", ["Smooth", "Aggressive"])

st.title("🚗 AI-Driven EV Range Predictor")
st.write("Real-time battery health and environmental impact analysis.")

# 3. Calculation Logic
if st.button("Calculate Performance"):
    health, km = estimate_ev_range(0.08, temp, style)
    
    # --- DASHBOARD LAYOUT START ---
    # Create two main columns: 1/3 for text/metrics, 2/3 for the graph
    col_left, col_right = st.columns([1, 2])

    with col_left:
        # 4. Display Metrics
        st.subheader("📊 Key Metrics")
        st.metric("Battery Health (SoH)", f"{health}%")
        st.metric("Estimated Range", f"{km} km")

        # 6. Alert System (Moved here to save vertical space)
        st.subheader("⚠️ System Status")
        if temp > 45:
            st.error(f"OVERHEATING: {temp}°C!")
        elif health < 30:
            st.error("LOW HEALTH!")
        else:
            st.success("SYSTEM OPTIMAL")

    with col_right:
        # 5. Visualization Module
        st.subheader("📈 Range Sensitivity")
        
        # Generate data
        temp_range = list(range(-10, 61, 5))
        ranges = [estimate_ev_range(0.08, t, style)[1] for t in temp_range]
        
        # Create a compact, responsive Plot
        # We use a smaller figsize and tight_layout to prevent scrolling
        fig, ax = plt.subplots(figsize=(7, 4)) 
        ax.plot(temp_range, ranges, marker='o', color='#1f77b4', linewidth=2)
        ax.axvline(x=temp, color='red', linestyle='--', label=f'Current: {temp}°C')
        
        ax.set_xlabel("Temp (°C)", fontsize=9)
        ax.set_ylabel("Range (km)", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(True, alpha=0.2)
        ax.legend(prop={'size': 8})
        
        plt.tight_layout() # Removes extra margins
        
        # use_container_width=True makes it fit the column perfectly
        st.pyplot(fig, use_container_width=True)
    # --- DASHBOARD LAYOUT END ---