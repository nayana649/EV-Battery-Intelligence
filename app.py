import streamlit as st
import matplotlib.pyplot as plt
from src.range_logic import estimate_ev_range

# 1. Page Configuration
st.set_page_config(
    page_title="EV Intelligence Hub", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MOBILE UI CLEAN-UP (CSS) ---
st.markdown("""
    <style>
    /* Hide Streamlit Branding and Menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* Optimize for Mobile Screens */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Make metrics look like App tiles */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1f77b4;
        font-weight: bold;
    }
    
    /* Custom button styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #1f77b4;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": "1234"}
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"
if 'show_graph' not in st.session_state:
    st.session_state.show_graph = False

# --- AUTHENTICATION ---
def auth_page():
    st.title("🚗 EV Intelligence")
    if st.session_state.auth_mode == "login":
        st.subheader("Login to your Account")
        with st.form("login_form"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Log In"):
                if u in st.session_state.user_db and st.session_state.user_db[u] == p:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        if st.button("New User? Create Account"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    else:
        st.subheader("Create Account")
        with st.form("signup_form"):
            new_u = st.text_input("New Username")
            new_p = st.text_input("New Password", type="password")
            if st.form_submit_button("Register"):
                st.session_state.user_db[new_u] = new_p
                st.session_state.auth_mode = "login"
                st.success("Account created!")
                st.rerun()

# --- PROFILE SETUP ---
def profile_setup():
    st.title("🛠️ Vehicle Selection")
    with st.form("setup"):
        brand_list = [
            "Tesla Model 3", "Tesla Model S", "Tata Nexon EV", "Tata Punch EV", 
            "Tata Tiago EV", "Ola S1 Pro", "Ather 450X", "TVS iQube", 
            "MG ZS EV", "MG Comet", "Mahindra XUV400", "Hyundai Ioniq 5", "BYD Atto 3"
        ]
        brand = st.selectbox("Select your EV Model", brand_list)
        if st.form_submit_button("Launch Dashboard"):
            st.session_state.user_data = {"brand": brand}
            st.rerun()

# --- MAIN DASHBOARD ---
def main_dashboard():
    brand = st.session_state.user_data.get('brand', "Tesla Model 3")
    st.title(f"⚡ {brand} Dashboard")

    # Sidebar
    st.sidebar.header("🔌 Live Sensors")
    voltage = st.sidebar.slider("Voltage (V)", 2.0, 4.5, 3.7)
    temp = st.sidebar.slider("Ambient Temp (°C)", -10, 60, 25)
    style = st.sidebar.selectbox("Driving Mode", ["Smooth", "Aggressive"])
    
    if st.sidebar.button("🔄 Switch Vehicle"):
        st.session_state.user_data = {}
        st.rerun()
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Backend Logic
    eff_const = 0.08 
    soc_factor = (voltage - 2.0) / (4.5 - 2.0)
    health, current_km = estimate_ev_range(eff_const, temp, style, brand)
    display_km = round(current_km * soc_factor, 2)

    # Layout
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📊 Metrics")
        st.metric("Range", f"{display_km} km")
        st.metric("Health", f"{health}%")
        
        if temp > 45: st.error("⚠️ Overheating!")
        elif soc_factor < 0.2: st.warning("⚠️ Low Battery!")
        else: st.success("✅ System Optimal")

    with col2:
        st.subheader(f"📈 Range Analysis")
        if st.button("🔍 Generate AI Graph"):
            st.session_state.show_graph = not st.session_state.show_graph

        if st.session_state.show_graph:
            temp_range = list(range(-10, 61, 5))
            ranges = [estimate_ev_range(eff_const, t, style, brand)[1] * soc_factor for t in temp_range]
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(temp_range, ranges, color='#1f77b4', marker='o', linewidth=2)
            ax.scatter(temp, display_km, color='red', s=100, zorder=5)
            ax.set_ylim(0, 700)
            ax.set_xlabel("Temp (°C)")
            ax.set_ylabel("Range (km)")
            st.pyplot(fig)
            plt.close(fig)

# --- APP NAVIGATION ---
if not st.session_state.logged_in:
    auth_page()
elif not st.session_state.user_data:
    profile_setup()
else:
    main_dashboard()
