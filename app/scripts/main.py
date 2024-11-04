from utils.constants import *
# Add the project root directory to the Python path
#sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# main.py
from scripts.reddit import fetch_and_store_reddit_posts as fetch_reddit_data
from scripts.news import fetch_and_store_news as fetch_news_data
from utils.error_handler import handle_error



def main():
    try:
    # Run news scraper
        fetch_news_data()
    # Fetch and store posts from each subreddit
        for subreddit in SUBREDDIT_LIST:
            fetch_reddit_data(subreddit)
    except Exception as e:
            handle_error(e)


if __name__ == "__main__":
    main()
