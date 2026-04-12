import streamlit as st
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 🔐 API KEY
API_KEY = "3dcc85d7b7b6005532a8993c26087b6c"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Weather AI Pro", layout="wide")

# ---------------- DARK MODE ----------------
theme = st.sidebar.selectbox("🌗 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {background-color: #0E1117; color: white;}
    </style>
    """, unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🌦 Weather AI Dashboard")
st.write("Real-time weather + AI prediction 🚀")

# ---------------- INPUT ----------------
city = st.sidebar.text_input("📍 Enter City", "Chandrapur")
compare = st.sidebar.text_input("🌍 Compare Cities (comma separated)", "")

# ---------------- FUNCTIONS ----------------
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None

# 🤖 AI MODEL
def predict_temperature(history):
    if len(history) < 3:
        return None

    X = np.array(range(len(history))).reshape(-1, 1)
    y = np.array(history)

    model = LinearRegression()
    model.fit(X, y)

    future = np.array([[len(history)]])
    prediction = model.predict(future)

    return round(prediction[0], 2)

# ---------------- BUTTON ----------------
if st.button("🚀 Get Weather Data"):

    data = get_weather(city)

    if data:
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        # ---------------- DISPLAY ----------------
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🌡 Temp", f"{temp}°C")
        col2.metric("☁ Weather", weather)
        col3.metric("💧 Humidity", f"{humidity}%")
        col4.metric("🌬 Wind", f"{wind} m/s")

        # ---------------- HISTORY ----------------
        if "temp_history" not in st.session_state:
            st.session_state.temp_history = []

        st.session_state.temp_history.append(temp)

        # ---------------- CHART ----------------
        df = pd.DataFrame({
            "Time": list(range(len(st.session_state.temp_history))),
            "Temp": st.session_state.temp_history
        })

        st.subheader("📊 Temperature Trend")
        st.line_chart(df.set_index("Time"))

        # ---------------- AI PREDICTION ----------------
        pred = predict_temperature(st.session_state.temp_history)

        if pred:
            st.subheader("🤖 AI Prediction")
            st.success(f"📈 Next Predicted Temperature: {pred} °C")

        # ---------------- FORECAST ----------------
        forecast = get_forecast(city)

        if forecast:
            st.subheader("📅 Forecast")

            temps = []
            times = []

            for item in forecast["list"][:8]:
                temps.append(item["main"]["temp"])
                times.append(item["dt_txt"])

            df2 = pd.DataFrame({"Time": times, "Temp": temps})
            st.line_chart(df2.set_index("Time"))

        # ---------------- MULTI CITY ----------------
        if compare:
            cities = [c.strip() for c in compare.split(",")]

            st.subheader("🌍 City Comparison")

            temps = []
            names = []

            for c in cities:
                d = get_weather(c)
                if d:
                    temps.append(d["main"]["temp"])
                    names.append(c)

            if temps:
                df3 = pd.DataFrame({"City": names, "Temp": temps})
                st.bar_chart(df3.set_index("City"))

    else:
        st.error("❌ Error fetching weather. Check API key.")