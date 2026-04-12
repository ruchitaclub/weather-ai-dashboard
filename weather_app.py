import requests
from plyer import notification
import time

# 🔐 API KEY
API_KEY = "3dcc85d7b7b6005532a8993c26087b6c"

# 🌍 Take city input (with default)
CITY = input("🌍 Enter city (default: Chandrapur): ")
if CITY.strip() == "":
    CITY = "Chandrapur"


# ---------------- GET WEATHER ----------------
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            return temp, weather, humidity, wind

        else:
            print("❌ API Error:", response.status_code)
            print("Response:", response.text)
            return None, None, None, None

    except requests.exceptions.RequestException as e:
        print("❌ Network Error:", e)
        return None, None, None, None


# ---------------- SEND NOTIFICATION ----------------
def send_notification(city, temp, weather, humidity, wind):
    try:
        notification.notify(
            title=f"🌦 Weather Update - {city}",
            message=f"🌡 Temp: {temp}°C\n☁ {weather}\n💧 {humidity}%\n🌬 {wind} m/s",
            timeout=10
        )
    except Exception as e:
        print("❌ Notification Error:", e)


# ---------------- SMART ALERTS ----------------
def smart_alerts(temp, weather):
    if temp is not None:
        if temp > 35:
            notification.notify(
                title="🔥 Heat Alert!",
                message="High temperature! Stay hydrated 💧",
                timeout=10
            )

        if "rain" in weather.lower():
            notification.notify(
                title="☔ Rain Alert!",
                message="Carry an umbrella!",
                timeout=10
            )


# ---------------- MAIN FUNCTION ----------------
def main():
    print("\n🚀 Weather Notifier Started...\n")

    while True:
        temp, weather, humidity, wind = get_weather(CITY)

        if temp is not None:
            print("📊 ==============================")
            print(f"🌍 City: {CITY}")
            print(f"🌡 Temperature: {temp}°C")
            print(f"☁ Weather: {weather}")
            print(f"💧 Humidity: {humidity}%")
            print(f"🌬 Wind Speed: {wind} m/s")
            print("📊 ==============================\n")

            send_notification(CITY, temp, weather, humidity, wind)
            smart_alerts(temp, weather)

        else:
            print("❌ Failed to fetch weather.\n")

        # ⏳ Wait or exit
        user = input("Press ENTER to continue or type 'exit' to stop: ")
        if user.lower() == "exit":
            print("👋 Exiting Weather Notifier...")
            break


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()