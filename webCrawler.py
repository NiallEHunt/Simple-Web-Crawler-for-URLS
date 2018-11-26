import argparse
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
    # if it runs into errors
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

if __name__ =='__main__':
    # Using a set as each element in a set can only appear once. Therefore, we end
    # up with a set of all the unique links
    unique_links = set()
    visited_links = set()

    parser = argparse.ArgumentParser(description="Scrape N unique URLs from an inputted URL. The default values are N = 100 and url = 'https://www.bbc.com'")

    parser.add_argument('-n', type=int, help="The number of unique URLs you want to find", default=100)
    parser.add_argument('-url', help="The starting URL to scrape from", default='https://www.bbc.com')

    args = parser.parse_args()

    url = args.url
    unique_links.add(url)
    upper_bound = args.n
    finished = False

    # Will find links from the given url. If the upper bound is not met it will use a random
    # url from the set to continue scraping from
    while not finished:
        unique_links = find_links_on_page(url, upper_bound, unique_links)

        visited_links.add(url)

        # If we have visited all the unique links we have found we break as we can't crawl through any more sites
        if visited_links == unique_links:
            break

        # The new url to scrape has to be one that we haven't visited before
        while url in visited_links:
            url = unique_links.pop()
            unique_links.add(url)

        if len(unique_links) >= upper_bound:
            finished = True

    # Print each url on a new line
    for link in unique_links:
        print(link)

    # If we didn't find N links print the number we found
    if len(unique_links) < upper_bound:
        print("Only found " + str(len(unique_links)) + " unique links")
