import urllib.robotparser

def is_scraping_allowed(user_agent, website_url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(website_url + '/robots.txt')
    rp.read()

    return rp.can_fetch(user_agent, website_url)

# Example usage
user_agent = 'apscrape/1.0'
website_url = 'https://espn.com'

allowed = is_scraping_allowed(user_agent, website_url)
if allowed:
    print("Scraping is allowed.")
else:
    print("Scraping is not allowed.")