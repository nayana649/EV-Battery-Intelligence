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
st.write("Visualizing real-time battery health and environmental impact.")

# 3. Calculation Logic
if st.button("Calculate Performance"):
    health, km = estimate_ev_range(0.08, temp, style)
    
    # 4. Display Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Battery Health (SoH)", f"{health}%")
    with col2:
        st.metric("Estimated Range", f"{km} km")

    # 5. Visualization Module (MEMBER 7 START)
    st.subheader("📊 Range Sensitivity Analysis")
    
    # Generate data for the graph
    temp_range = list(range(-10, 61, 5))
    ranges = [estimate_ev_range(0.08, t, style)[1] for t in temp_range]
    
    # Create the Plot
    fig, ax = plt.subplots()
    ax.plot(temp_range, ranges, marker='o', color='#1f77b4', linewidth=2)
    ax.axvline(x=temp, color='red', linestyle='--', label=f'Current Temp: {temp}°C')
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Estimated Range (km)")
    ax.set_title(f"Impact of Temperature on {style} Driving Range")
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Display Graph in Streamlit
    st.pyplot(fig)
    # (MEMBER 7 END)

    # 6. Alert System
    st.subheader("⚠️ System Alerts & Suggestions")
    if temp > 45:
        st.error(f"ALERT: Battery Overheating ({temp}°C)!")
    elif health < 30:
        st.error("CRITICAL: Low Battery Health!")
    else:
        st.success("SYSTEM READY: Battery is in optimal condition.")