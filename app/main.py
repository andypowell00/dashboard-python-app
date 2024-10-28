import sys
import os
from utils.constants import *
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# main.py
from scripts.reddit import fetch_and_store_reddit_posts as fetch_reddit_data
from scripts.news import fetch_and_store_news as fetch_news_data
from scripts.weather import fetch_and_store_weather_data
from utils.error_handler import handle_error



def main():
   
    # Run news scraper
    #fetch_news_data()

    
    # Fetch and store posts from each subreddit
    #for subreddit in SUBREDDIT_LIST:
    #    fetch_reddit_data(subreddit)

    # Fetch weather data for a specific latitude and longitude
    fetch_and_store_weather_data(lat=40.1157, lon=-83.1327)  


if __name__ == "__main__":
    main()
