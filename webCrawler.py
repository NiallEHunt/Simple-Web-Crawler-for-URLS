import requests
from bs4 import BeautifulSoup

# Finds all the links on the given page and adds them to the unique_links set
# returns True if the unique_links set is full (ie. has N links)
# returns False if the unique_links set is not full (ie. less than N links)
def find_links_on_page(url, N):
    # Use requests to get the raw text of the page
    raw_data = requests.get(url).text

    # Use BeautifulSoup to scrape the a tags
    scraper = BeautifulSoup(raw_data, "html.parser")
    for tag in scraper.findAll('a'):
        link = tag.get('href')

        # If the link doesn't start with http it must be a relative link
        # ie a link to another page with the same base url
        if link[:4] != 'http':
            link = url + link

        unique_links.add(link)
        # Once we have found N unique_links return True
        if len(unique_links) >= N:
            return True

    return False

# Using a set as each element in a set can only appear once. Therefore, we end
# up with a set of all the unique links
unique_links = set()

# Set the upper bound of the set (ie. how many unique urls you want to print)
upper_bound = 150
finished = False
url = 'https://www.youtube.com/watch?v=oYqyzctGCHs'
while not finished:
    finished = find_links_on_page(url, upper_bound)
    url = unique_links.pop()
    unique_links.add(url)
for link in unique_links:
    print(link)
