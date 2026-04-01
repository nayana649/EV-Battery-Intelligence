# 🚗 AI-Driven Adaptive Battery Intelligence & Range Prediction System

An advanced AI-powered web application designed to predict Electric Vehicle (EV) battery health (SoH) and real-time range estimation based on environmental and behavioral factors.

## 🌟 Key Features
* **Secure Authentication:** User login and registration system to protect vehicle data.
* **Profile Management:** Custom vehicle registration for different EV brands (Tesla, Tata, Ola, etc.).
* **Real-time Analytics:** * 🔋 **Battery Health (SoH):** Predicts degradation based on usage patterns.
    * 🚗 **Range Estimation:** Dynamic calculation based on Voltage and Temperature.
* **Smart Alerts:** Automated warnings for overheating or critical battery health.
* **Interactive Visualizations:** Temperature sensitivity graphs to analyze range impact.

## 🛠️ Tech Stack
* **Frontend/Backend:** [Streamlit](https://streamlit.io/)
* **Language:** Python 3.x
* **Data Science:** Pandas, NumPy, Matplotlib
* **Deployment:** Streamlit Cloud / GitHub

## 📂 Project Structure
```text
EV_Battery_Project/
├── app.py              # Main Streamlit application (UI & Navigation)
├── src/
│   └── range_logic.py  # Core AI & Range Calculation logic
├── requirements.txt    # Python dependencies
├── app_icon.png        # App branding icon
└── README.md           # Project documentation

1. Operational Logic (The "Brain" of the App)
This explains the step-by-step process your code follows:
Data Input: User provides Voltage, Temperature, and Driving Style.
AI Processing: ML model analyzes patterns like high-temperature damage and charge cycles.
Outputs: Real-time prediction of Battery Health (SoH %) and Range Calculation.

2. Team Contributions
Since you have a large team, explicitly listing the roles ensures everyone gets credit for their module:
Data & AI Team (Members 1-4): Dataset preparation and ML model training.
Logic & App Team (Members 5-7): Range formulas, Streamlit UI, and Dashboard visualization.

3. Future Scope
To show you are thinking like a real engineer, mention what comes next:
Database Integration: Moving from temporary session storage to a permanent database (like Firebase) for user accounts.
Hardware Connection: Integrating the app with real-time OBD-II sensors to pull live data from an actual EV.
