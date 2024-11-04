from scripts.weather import fetch_and_store_weather_data
from utils.constants import *
from utils.error_handler import handle_error

def main():
    try:
        # Run the weather data fetch
        fetch_and_store_weather_data(lat=40.1157, lon=-83.1327)
    except Exception as e:
        handle_error(e)

if __name__ == "__main__":
    main()  # This will execute the main function when the script is run directly.
