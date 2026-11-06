import csv, json, time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

with open('dataset.csv') as f:
    for row in csv.DictReader(f):
        event = {'reading_time': row['Date_Time'],
                 'global_active_power': float(row['Global_active_power'])}
        producer.send('smartmeter-events', value=event)
        print(f"Sent: {event}")
        time.sleep(0.2)
