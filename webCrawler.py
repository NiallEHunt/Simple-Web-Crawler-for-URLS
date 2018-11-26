import argparse
from fetch import find_links_on_page

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
