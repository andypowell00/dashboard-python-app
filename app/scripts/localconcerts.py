import requests
import json
import logging
from config.logerrors import configure_logging
from bs4 import BeautifulSoup
from utils.constants import *

configure_logging()

try:
# URL of the website to scrape
    url = LOCAL_CONCERT_LIST

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the <p> tags
    p_tags = soup.find_all("p")

    # Extract the date, venue, and activity from each <p> tag
    events = []
    for p_tag in p_tags:
        text = p_tag.get_text().strip()
        if ":" in text:
            venue, venue_activity = text.split("\n", 1)
            date, activity = venue_activity.split(": ", 1)
            if venue is not None and venue != "Streaming/Online Events":
                events.append({
                    "date": date,
                    "venue": venue,
                    "activity": activity
                })

    # Print the extracted events
    for event in events:
        print("Date:", event["date"])
        print("Venue:", event["venue"])
        print("Activity:", event["activity"])
        print()

# Save the events data to a JSON file
    with open("events.json", "w") as file:
        json.dump(events, file, indent=4)

except requests.exceptions.RequestException as e:
    logging.error(f"Failed to retrieve website content: {e}")

except Exception as e:
    logging.error(f"An error occurred: {e}")