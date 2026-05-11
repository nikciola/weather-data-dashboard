import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"

CITY = {
    "name": "Krakow",
    "latitude": 50.06,
    "longitude": 19.94
}


def fetch_weather_data():
    params = {
        "latitude": CITY["latitude"],
        "longitude": CITY["longitude"],
        "hourly": "temperature_2m",
        "forecast_days": 1
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    return response.json()


def process_data(data):
    times = data["hourly"]["time"]
    temperatures = data["hourly"]["temperature_2m"]

    df = pd.DataFrame({
        "time": times,
        "temperature": temperatures
    })

    df["time"] = pd.to_datetime(df["time"])

    return df


def save_to_csv(df):
    df.to_csv("weather_data.csv", index=False)
    print("CSV file created.")


def save_to_database(df):
    conn = sqlite3.connect("weather.db")
    df.to_sql("weather", conn, if_exists="replace", index=False)
    conn.close()

    print("SQLite database created.")


def create_chart(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["temperature"], marker="o")

    plt.title("Temperature Forecast - Krakow")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig("temperature_chart.png")

    print("Chart saved.")


def print_summary(df):
    print("\nWEATHER DATA SUMMARY")
    print("====================")
    print(f"Average temperature: {df['temperature'].mean():.2f} °C")
    print(f"Max temperature: {df['temperature'].max():.2f} °C")
    print(f"Min temperature: {df['temperature'].min():.2f} °C")


def main():
    print("Fetching weather data...")

    weather_data = fetch_weather_data()
    df = process_data(weather_data)

    save_to_csv(df)
    save_to_database(df)
    create_chart(df)
    print_summary(df)

    print("\nProject completed successfully.")


if __name__ == "__main__":
    main()
