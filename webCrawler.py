import requests
from bs4 import BeautifulSoup

def find_links_on_page(url):
    raw_data = requests.get(url).text
    scraper = BeautifulSoup(raw_data, "html.parser")
    for tag in scraper.findAll('a'):
        link = tag.get('href')
        print(link)

find_links_on_page('http://www.bbc.com')
