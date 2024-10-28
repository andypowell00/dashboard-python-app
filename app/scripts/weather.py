import os
import requests
import logging
from pymongo import MongoClient
from datetime import datetime
from utils.logging_config import configure_logging
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

configure_logging()

# OpenWeatherMap API key and base URL
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# MongoDB connection settings
MONGO_URI = os.getenv('MONGO_URI')   
DATABASE_NAME = os.getenv('MONGO_DB_NAME')
COLLECTION_NAME = "Weather"

def fetch_and_store_weather_data(lat, lon):
    try:
        # Build the request URL for the 5-day forecast
        url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
        
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the JSON response
        data = response.json()

        # Dictionary to hold daily summaries
        daily_weather = {}

        # Iterate through the forecast data
        for forecast in data["list"]:
            # Extract date
            date_str = datetime.fromtimestamp(forecast["dt"]).strftime("%Y-%m-%d")
            
            # If the date is not already in the dictionary, add it
            if date_str not in daily_weather:
                daily_weather[date_str] = {
                    "status": forecast["weather"][0]["description"],
                    "high_temp": forecast["main"]["temp_max"],
                    "low_temp": forecast["main"]["temp_min"]
                }
            else:
                # Update the high and low temperatures if needed
                daily_weather[date_str]["high_temp"] = max(daily_weather[date_str]["high_temp"], forecast["main"]["temp_max"])
                daily_weather[date_str]["low_temp"] = min(daily_weather[date_str]["low_temp"], forecast["main"]["temp_min"])

        # Connect to MongoDB and insert the weather data for each day
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        for date, weather in daily_weather.items():
            weather_data = {
                "date": date,
                "status": weather["status"],
                "high_temp": weather["high_temp"],
                "low_temp": weather["low_temp"],
                "lat": lat,
                "lon": lon
            }
            collection.insert_one(weather_data)

        logging.info("Weather data successfully inserted into MongoDB.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch weather data: {e}")
    except KeyError as e:
        logging.error(f"Unexpected data format: {e}")
    except Exception as e:
        logging.error(f"Failed to insert data into MongoDB: {e}")