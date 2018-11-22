import requests
from bs4 import BeautifulSoup

unique_links = set()

def find_links_on_page(url):
    raw_data = requests.get(url).text
    scraper = BeautifulSoup(raw_data, "html.parser")
    for tag in scraper.findAll('a'):
        link = tag.get('href')
        if link[:4] != 'http':
            link = url + link
        unique_links.add(link)

find_links_on_page('http://www.bbc.com')
for link in unique_links:
    print(link)
