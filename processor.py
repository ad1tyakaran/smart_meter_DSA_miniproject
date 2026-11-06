import joblib, json
from collections import deque
from kafka import KafkaConsumer
import mysql.connector

conn = mysql.connector.connect(host='localhost', user='meter_app', password='meter_pass', database='smartmeter')
cursor = conn.cursor()

model = joblib.load('anomaly_model.pkl')
window = deque(maxlen=30)
peak = 0.0

consumer = KafkaConsumer('smartmeter-events', bootstrap_servers='127.0.0.1:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

print("Processor started, waiting for events...")
for message in consumer:
    power = message.value['global_active_power']
    reading_time = message.value['reading_time']
    
    window.append(power)
    rolling_avg = sum(window) / len(window) 
    peak = max(peak, power)
    
    prediction = model.predict([[power]])[0]
    is_anomaly = 1 if prediction == -1 else 0
    
    cursor.execute("""
        INSERT INTO meter_readings (reading_time, global_active_power, rolling_avg_30, is_anomaly)
        VALUES (%s, %s, %s, %s)
    """, (reading_time, power, rolling_avg, is_anomaly))
    conn.commit()
    print(f"Processed: {reading_time}, Power: {power}, Anomaly: {is_anomaly}")
