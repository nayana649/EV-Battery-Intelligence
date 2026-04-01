import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. Load the Prepared Data (Created by Members 1 & 2)
df = pd.read_csv('data/Prepared_EV_Data.csv')

# 2. FIX: Use the correct column names from your specific dataset
# We use 'Re' (Resistance), 'Rct' (Transfer Resistance), and 'ambient_temperature'
X = df[['Re', 'Rct', 'ambient_temperature', 'test_id']]
y = df['SoH_Percentage']

# 3. Split into Training and Testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the AI Model
print("🤖 Training the Battery Intelligence Model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Check Accuracy
predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)
print(f"✅ Training Complete! Average Error: {error:.4f}%")

# 6. Ensure 'models' folder exists and SAVE THE MODEL
if not os.path.exists('models'):
    os.makedirs('models')

with open('models/battery_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("💾 Model saved as 'models/battery_model.pkl'")