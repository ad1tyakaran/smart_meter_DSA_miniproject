# Real-Time Streaming Analytics Mini-Project

## Project Contents
* `schema.sql` - MySQL Database schema setup.
* `train_model.py` - Scikit-Learn script to train the IsolationForest ML model.
* `producer.py` - Kafka script to read CSV data and send it as a live stream.
* `processor.py` - Kafka consumer that manages sliding windows, scores data, and writes to MySQL. 
* `dashboard.py` - Streamlit app for the auto-refreshing live visualization.
* `dataset.csv` - Small sample electricity dataset for testing. 

## Prerequisites
1. **Kafka**: Download and extract Apache Kafka. You need ZooKeeper and the Kafka Server running.
2. **MySQL**: Install MySQL and ensure the service is running.
3. **Python**: Python 3.8+ recommended.

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install kafka-python scikit-learn pandas mysql-connector-python streamlit joblib
```

### 2. Database Setup
Log into your MySQL terminal and create the database and user:
```sql
CREATE DATABASE smartmeter;
CREATE USER 'meter_app'@'localhost' IDENTIFIED BY 'meter_pass';
GRANT ALL PRIVILEGES ON smartmeter.* TO 'meter_app'@'localhost';
FLUSH PRIVILEGES;
```
Then run the `schema.sql` file to create the table structure:
```bash
mysql -u meter_app -pmeter_pass smartmeter < schema.sql
```

### 3. Start Kafka (In separate terminal tabs)
```bash
# Terminal 1: Start ZooKeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Terminal 2: Start Kafka Server
bin/kafka-server-start.sh config/server.properties
```

Create the Kafka topic:
```bash
bin/kafka-topics.sh --create --topic smartmeter-events --bootstrap-server localhost:9092
```

## Running the Pipeline

Run these scripts in **separate terminal windows/tabs** so they operate concurrently:

1. **Train the ML Model**
   ```bash
   python train_model.py
   ```

2. **Start the Stream Processor**
   ```bash
   python processor.py
   ```

3. **Start the Live Dashboard**
   ```bash
   streamlit run dashboard.py
   ```

4. **Start the Producer (Data stream)**
   ```bash
   python producer.py
   ```
