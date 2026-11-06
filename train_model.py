from sklearn.ensemble import IsolationForest
import joblib, pandas as pd

df = pd.read_csv('dataset.csv', usecols=['Global_active_power']).dropna()
model = IsolationForest(contamination=0.01, random_state=42)
model.fit(df[['Global_active_power']])
joblib.dump(model, 'anomaly_model.pkl')
print("Model trained and saved as anomaly_model.pkl")
