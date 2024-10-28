import requests
import logging
import os
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from utils.logging_config import configure_logging
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

configure_logging()

base_url = "https://news.mit.edu"

# MongoDB connection details
MONGO_URI = os.getenv('MONGO_URI')  # Change this to your MongoDB URI if different
DATABASE_NAME = os.getenv('MONGO_DB_NAME')
COLLECTION_NAME = "News"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
news_collection = db[COLLECTION_NAME]

def get_headline_urls(news_url, keywords):
    try:
        response = requests.get(news_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        headline_urls = []
        for headline in soup.find_all('a'):
            headline_text = headline.get_text().lower()
            if any(keyword in headline_text for keyword in keywords):
                url = headline.get('href')
                if url is not None:
                    headline_urls.append(url)
        return headline_urls
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve website content: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

def get_article_details(article_url):
    try:
        full_url = base_url + article_url
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get article body
        article_body = soup.find('article').text.strip() if soup.find('article') else "No content available"

        # Get image URL if available
        image_url = None
        image_tag = soup.find('img')
        if image_tag:
            image_url = image_tag.get('src')

        return {
            "url": full_url,
            "body": article_body,
            "image_url": image_url,
            "date": datetime.today().strftime('%Y-%m-%d')  # Add the current date
        }
    except Exception as e:
        logging.error(f"An error occurred while retrieving article details: {e}")
        return None

def save_article_to_mongo(article_details):
    try:
        if article_details:
            # Insert the article into the News collection
            news_collection.insert_one(article_details)
            logging.info(f"Article saved to MongoDB: {article_details['url']}")
        else:
            logging.warning("No article details provided to save.")
    except Exception as e:
        logging.error(f"Failed to save article to MongoDB: {e}")

def fetch_and_store_news():
    # Example usage
    news_url = 'https://news.mit.edu/topic/artificial-intelligence2'
    keywords = ['generative', 'artificial intelligence', 'deep learning', 'machine learning', 'ai', 'network']

    headline_urls = get_headline_urls(news_url, keywords)
    if headline_urls:
        for url in headline_urls:
            if url and "http" not in url:
                article_details = get_article_details(url)
                if article_details:
                    save_article_to_mongo(article_details)
