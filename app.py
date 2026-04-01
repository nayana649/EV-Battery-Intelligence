import streamlit as st
import matplotlib.pyplot as plt
from src.range_logic import estimate_ev_range

# 1. Page Configuration
st.set_page_config(page_title="EV Intelligence", page_icon="app_icon.png", layout="wide")

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": "1234"} # Default account
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"

# --- AUTHENTICATION PAGE ---
def auth_page():
    st.title("🚗 EV Intelligence App")
    if st.session_state.auth_mode == "login":
        st.subheader("Login to your Account")
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if u in st.session_state.user_db and st.session_state.user_db[u] == p:
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("Invalid credentials")
        if st.button("New User? Create Account"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    else:
        st.subheader("Create Account")
        with st.form("signup"):
            new_u = st.text_input("New Username")
            new_p = st.text_input("New Password", type="password")
            if st.form_submit_button("Register"):
                st.session_state.user_db[new_u] = new_p
                st.session_state.auth_mode = "login"
                st.success("Account created!")
                st.rerun()

# --- PROFILE SETUP ---
def profile_setup():
    st.title("🛠️ Vehicle Registration")
    with st.form("setup"):
        name = st.text_input("EV Name (e.g. My Ola S1)")
        brand = st.selectbox("Brand", ["Ola", "Ather", "TVS", "Tesla", "Tata", "Other"])
        if st.form_submit_button("Start Dashboard"):
            st.session_state.user_data = {"name": name, "brand": brand}
            st.rerun()

# --- MAIN DASHBOARD (FULL FEATURES) ---
def main_dashboard():
    details = st.session_state.user_data
    st.title(f"⚡ {details['name']} Performance Hub")

    # --- SIDEBAR: USER INPUTS ---
    st.sidebar.header("🔌 Live Parameters")
    voltage = st.sidebar.slider("Voltage (V)", 2.0, 4.5, 3.7)
    temp = st.sidebar.slider("Ambient Temperature (°C)", -10, 60, 25)
    style = st.sidebar.selectbox("Driving Style", ["Smooth", "Aggressive"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_data = {}
        st.rerun()

    # --- CALCULATION LOGIC ---
    # Assuming 0.08 is your standard internal resistance or coefficient
    health, km = estimate_ev_range(0.08, temp, style)

    # --- APP LAYOUT ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📊 Key Metrics")
        st.metric("Estimated Range", f"{km} km")
        st.metric("Battery Health (SoH)", f"{health}%")
        st.metric("Operating Voltage", f"{voltage} V")

        st.subheader("⚠️ System Status")
        if temp > 45:
            st.error(f"ALERT: Battery Overheating ({temp}°C)!")
        elif health < 30:
            st.error("CRITICAL: Low Battery Health!")
        else:
            st.success("SYSTEM READY: Battery Optimal")

    with col2:
        st.subheader("📈 Range Sensitivity Analysis")
        # Generate full sensitivity data for the graph
        temp_range = list(range(-10, 61, 5))
        ranges = [estimate_ev_range(0.08, t, style)[1] for t in temp_range]
        
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(temp_range, ranges, marker='o', color='#1f77b4', linewidth=2)
        ax.axvline(x=temp, color='red', linestyle='--', label=f'Current: {temp}°C')
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Range (km)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig, use_container_width=True)

# --- NAVIGATION ---
if not st.session_state.logged_in:
    auth_page()
elif not st.session_state.user_data:
    profile_setup()
else:
    main_dashboard()