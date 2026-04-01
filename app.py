import streamlit as st
import matplotlib.pyplot as plt
from src.range_logic import estimate_ev_range

# 1. Page Configuration
st.set_page_config(page_title="EV Intelligence", page_icon="app_icon.png", layout="wide")

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_db' not in st.session_state:
    # Pre-filling one admin account for testing
    st.session_state.user_db = {"admin": "1234"} 
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"

# --- FUNCTION: AUTHENTICATION (Login/Signup) ---
def auth_page():
    st.title("🚗 EV Intelligence App")
    
    if st.session_state.auth_mode == "login":
        st.subheader("Login to your Account")
        with st.form("login_form"):
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if user in st.session_state.user_db and st.session_state.user_db[user] == pw:
                    st.session_state.logged_in = True
                    st.success(f"Welcome back, {user}!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        if st.button("New User? Create Account"):
            st.session_state.auth_mode = "signup"
            st.rerun()

    else:
        st.subheader("Create a New Account")
        with st.form("signup_form"):
            new_user = st.text_input("Choose Username")
            new_pw = st.text_input("Choose Password", type="password")
            confirm_pw = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Register"):
                if new_user in st.session_state.user_db:
                    st.error("Username already exists!")
                elif new_pw != confirm_pw:
                    st.error("Passwords do not match!")
                elif len(new_user) < 3 or len(new_pw) < 4:
                    st.error("Username/Password too short!")
                else:
                    st.session_state.user_db[new_user] = new_pw
                    st.session_state.auth_mode = "login"
                    st.success("Account created! Please login.")
                    st.rerun()
        
        if st.button("Already have an account? Login"):
            st.session_state.auth_mode = "login"
            st.rerun()

# --- FUNCTION: PROFILE SETUP ---
def profile_setup():
    st.title("🛠️ Set Up Your EV Profile")
    with st.form("profile_form"):
        ev_name = st.text_input("Vehicle Name (e.g., My Tata Nexon)")
        brand = st.selectbox("Manufacturer", ["Tata", "Tesla", "Mahindra", "Hyundai", "BYD", "Other"])
        if st.form_submit_button("Launch Dashboard"):
            st.session_state.user_data = {"name": ev_name, "brand": brand}
            st.rerun()

# --- FUNCTION: MAIN DASHBOARD ---
def main_dashboard():
    u_name = st.session_state.user_data['name']
    st.title(f"📊 {u_name} Live Stats")
    
    # Sidebar for logout and settings
    st.sidebar.title("App Settings")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_data = {}
        st.rerun()

    # Calculation UI (Your original logic)
    temp = st.sidebar.slider("Temperature (°C)", -10, 60, 25)
    style = st.sidebar.selectbox("Driving Style", ["Smooth", "Aggressive"])
    health, km = estimate_ev_range(0.08, temp, style)
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Range Remaining", f"{km} km")
        st.metric("Battery Health", f"{health}%")
    with c2:
        # Mini chart
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot([0, 10, 20, 30], [km, km*0.8, km*0.6, km*0.4], color='green')
        st.pyplot(fig)

# --- APP FLOW CONTROL ---
if not st.session_state.logged_in:
    auth_page()
elif not st.session_state.user_data:
    profile_setup()
else:
    main_dashboard()