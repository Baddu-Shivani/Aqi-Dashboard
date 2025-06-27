
import pandas as pd
import streamlit as st
import plotly.express as px
import os

st.set_page_config(page_title="Hyderabad AQI Dashboard", layout="wide")

st.title("🌫️ Hyderabad Air Quality Index Dashboard")

LOG_CSV = "aqi_log.csv"

if not os.path.exists(LOG_CSV):
    st.warning("Log file not found. Please upload aqi_log.csv")
    st.stop()

df = pd.read_csv(LOG_CSV)
df['date'] = pd.to_datetime(df['date'])
df.sort_values('date', inplace=True)

st.sidebar.header("📅 Date Range")
date_min = st.sidebar.date_input("From", df['date'].min().date())
date_max = st.sidebar.date_input("To", df['date'].max().date())
filtered = df[(df['date'] >= pd.to_datetime(date_min)) & (df['date'] <= pd.to_datetime(date_max))]

avg_aqi = filtered['predicted_aqi_tomorrow'].mean()
max_aqi = filtered['predicted_aqi_tomorrow'].max()
min_aqi = filtered['predicted_aqi_tomorrow'].min()

col1, col2, col3 = st.columns(3)
col1.metric("📈 Average Predicted AQI", f"{avg_aqi:.2f}")
col2.metric("🔴 Highest AQI", f"{max_aqi:.2f}")
col3.metric("🟢 Lowest AQI", f"{min_aqi:.2f}")

st.subheader("📊 Predicted AQI Over Time")
fig = px.line(filtered, x='date', y='predicted_aqi_tomorrow', markers=True, title="AQI Prediction Trend")
fig.update_traces(line_color='#FF4B4B')
st.plotly_chart(fig, use_container_width=True)

st.subheader("📉 Pollutant Levels Over Time")
pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
selected_pollutant = st.selectbox("Select Pollutant", pollutants)
fig2 = px.line(filtered, x='date', y=selected_pollutant, markers=True, title=f"{selected_pollutant} Trend")
fig2.update_traces(line_color='#1f77b4')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📄 Logged Data Table")
st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
