import streamlit as st
import matplotlib.pyplot as plt
from src.range_logic import estimate_ev_range

# 1. Page Configuration
st.set_page_config(page_title="EV Intelligence", page_icon="app_icon.png", layout="wide")

# Initialize Session State (This keeps track of login status)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# --- FUNCTION: LOGIN PAGE ---
def login_page():
    st.title("🔐 Secure Member Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            # Simple demo logic: (In a real app, you'd check a database)
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun() # Refresh to show the next page
            else:
                st.error("Invalid Username or Password")

# --- FUNCTION: PROFILE SETUP ---
def profile_setup():
    st.title("🚗 Complete Your EV Profile")
    st.info("Please enter your vehicle details to continue.")
    
    with st.form("profile_form"):
        ev_name = st.text_input("EV Model Name (e.g., Nexon EV, Tesla Model 3)")
        brand = st.selectbox("Brand", ["Tata", "Tesla", "Mahindra", "Hyundai", "Other"])
        battery_cap = st.number_input("Battery Capacity (kWh)", min_value=10, max_value=150, value=30)
        
        if st.form_submit_button("Save & Enter Dashboard"):
            st.session_state.user_data = {"name": ev_name, "brand": brand, "cap": battery_cap}
            st.rerun()

# --- FUNCTION: MAIN DASHBOARD (Your Original App) ---
def main_dashboard():
    data = st.session_state.user_data
    st.title(f"🚗 {data['name']} Dashboard")
    st.write(f"Welcome back! Analyzing your **{data['brand']}** with {data['cap']}kWh battery.")

    # Sidebar Inputs
    st.sidebar.header("🔌 Live Parameters")
    temp = st.sidebar.slider("Ambient Temperature (°C)", -10, 60, 25)
    style = st.sidebar.selectbox("Driving Style", ["Smooth", "Aggressive"])

    # Calculation & Layout (Same as before)
    health, km = estimate_ev_range(0.08, temp, style)
    
    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.subheader("📊 Key Metrics")
        st.metric("Battery Health (SoH)", f"{health}%")
        st.metric("Estimated Range", f"{km} km")
        if temp > 45: st.error("⚠️ OVERHEATING!")
        else: st.success("✅ SYSTEM OPTIMAL")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = {}
            st.rerun()

    with col_right:
        st.subheader("📈 Range Analysis")
        temp_range = list(range(-10, 61, 5))
        ranges = [estimate_ev_range(0.08, t, style)[1] for t in temp_range]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(temp_range, ranges, marker='o', color='#1f77b4')
        ax.grid(True, alpha=0.2)
        st.pyplot(fig, use_container_width=True)

# --- MAIN NAVIGATION LOGIC ---
if not st.session_state.logged_in:
    login_page()
elif not st.session_state.user_data:
    profile_setup()
else:
    main_dashboard()