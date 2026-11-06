import streamlit as st, pandas as pd, mysql.connector

st.set_page_config(page_title="Smart Meter Analytics", layout="wide")
st.title("Smart Meter Real-Time Streaming Analytics")

st.markdown("<meta http-equiv='refresh' content='2'>", unsafe_allow_html=True)

conn = mysql.connector.connect(host='localhost', user='meter_app', password='meter_pass', database='smartmeter')

recent = pd.read_sql('SELECT reading_time, global_active_power, rolling_avg_30, is_anomaly FROM meter_readings ORDER BY reading_pk DESC LIMIT 120', conn)

if not recent.empty:
    latest = recent.iloc[0]
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Current Power", f"{latest['global_active_power']:.3f} kW")
    col2.metric("30-min Avg", f"{latest['rolling_avg_30']:.3f} kW")
    col3.metric("Peak Power", f"{recent['global_active_power'].max():.3f} kW")
    col4.metric("Total Readings", len(recent))
    col5.metric("Anomalies", recent['is_anomaly'].sum())
    
    st.line_chart(recent.set_index('reading_time')[['global_active_power','rolling_avg_30']])
else:
    st.write("Waiting for data...")
