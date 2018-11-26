import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Request retry session code taken from https://www.peterbe.com/plog/best-practice-with-retries-with-requests
# Credit: Peter Bengtsson
def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Finds all the links on the given page and adds them to the unique_links set
# returns True if the unique_links set is full (ie. has N links)
# returns False if the unique_links set is not full (ie. less than N links)
def find_links_on_page(url, N, unique_links):
    # Use the requset retry session above to get the raw html of the page and retry
    # if it runs into errors. This drastically slows down the program but is
    # a lot more robust
    try:
        raw_data = requests_retry_session().get(url).text
    except:
        print("Invalid url")
        return unique_links

    # Use BeautifulSoup to scrape the a tags
    scraper = BeautifulSoup(raw_data, "html.parser")
    for tag in scraper.findAll('a'):
        link = tag.get('href')

        # If the link is None continue in the loop and look for the next valid link
        if link is None:
            continue

        unique_links.add(urljoin(url, link))
        # Once we have found N unique_links return True
        if len(unique_links) >= N:
            return unique_links

    return unique_links
