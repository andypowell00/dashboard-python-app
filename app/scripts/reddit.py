import logging
from utils.error_handler import handle_error
import praw  # Reddit API wrapper
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from utils.logging_config import configure_logging

# Load environment variables from the .env file
load_dotenv()
configure_logging()

# Set up Reddit client
reddit = praw.Reddit(
    client_id= os.getenv('REDDIT_CLIENT_ID'),
    client_secret= os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent= os.getenv('REDDIT_USER_AGENT')
)


# MongoDB setup
mongo_client = MongoClient(os.getenv('MONGO_URI'))
db = mongo_client[os.getenv('MONGO_DB_NAME')]
collection = db["RedditPosts"]

def fetch_and_store_reddit_posts(subreddit_name, post_limit=5):
    try:
    # Fetch posts from the specified subreddit
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.hot(limit=post_limit)

        # List to hold post data
        post_data = []
        
        for post in posts:
            # Check if the post URL points to an image
            image_url = post.url if post.url.endswith(('.jpg', '.png', '.gif', '.jpeg','.img')) else None

            post_info = {
                "title": post.title,
                "url": post.url,
                "score": post.score,
                "created_utc": post.created_utc,
                "subreddit": post.subreddit.display_name,
                "author": str(post.author),
                "selftext": post.selftext,
                "image_url": image_url
            }
            post_data.append(post_info)

        # Insert posts into MongoDB
        if post_data:
            collection.insert_many(post_data)
            print(f"Inserted {len(post_data)} posts into the 'RedditPosts' collection.")
            logging.info(f"Reddit posts inserted.")
        else:
            print("No posts found.")
            logging.info(f"No posts found.")
    except Exception as e:
        handle_error(e, "Fetch from Reddit failed.")

    
