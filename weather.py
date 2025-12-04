import threading
import time
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -----------------------------
# Dataclass for Weather Info
# -----------------------------
@dataclass
class WeatherData:
    city: str
    temp: float
    humidity: int
    description: str
    fetched_at: datetime


# -----------------------------
# Simple In-Memory Cache
# -----------------------------
class Cache:
    def __init__(self):
        self.store = {}
        self.ttl = timedelta(seconds=20)  # cache valid for 20 sec

    def set(self, key, value):
        self.store[key] = (value, datetime.now())
        logging.info(f"Cached data for {key}")

    def get(self, key):
        if key not in self.store:
            return None
        
        data, timestamp = self.store[key]
        if datetime.now() - timestamp > self.ttl:
            logging.info(f"Cache expired for {key}")
            del self.store[key]
            return None
        
        logging.info(f"Using cached data for {key}")
        return data


# -----------------------------
# Weather Client
# -----------------------------
class WeatherClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather(self, city):
        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude=28.6&longitude=77.2&current_weather=true"
            )  # Using static coords for example (Delhi)

            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()["current_weather"]

            return WeatherData(
                city=city,
                temp=data["temperature"],
                humidity=data.get("relativehumidity", 40),
                description="Clear Sky",
                fetched_at=datetime.now(),
            )

        except Exception as e:
            logging.error(f"Failed to fetch weather for {city}: {e}")
            return None


# -----------------------------
# Weather Manager (Threaded)
# -----------------------------
class WeatherManager:
    def __init__(self, cities, api_key):
        self.cities = cities
        self.cache = Cache()
        self.client = WeatherClient(api_key)

    def get_weather(self, city):
        cached = self.cache.get(city)
        if cached:
            return cached

        data = self.client.fetch_weather(city)
        if data:
            self.cache.set(city, data)
        return data

    def fetch_all(self):
        threads = []
        results = {}

        def worker(city):
            results[city] = self.get_weather(city)

        for city in self.cities:
            thread = threading.Thread(target=worker, args=(city,))
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

        return results


# -----------------------------
# Main Runner
# -----------------------------
if __name__ == "__main__":
    cities = ["Delhi", "Mumbai", "Bangalore"]

    wm = WeatherManager(cities, api_key="dummy-key")

    data = wm.fetch_all()

    print("\n==== WEATHER REPORT ====\n")
    for city, w in data.items():
        if w:
            print(f"🌆 City: {w.city}")
            print(f"🌡 Temperature: {w.temp}°C")
            print(f"💧 Humidity: {w.humidity}%")
            print(f"📄 Description: {w.description}")
            print(f"⏱ Fetched At: {w.fetched_at}")
            print("-------------------------------")
