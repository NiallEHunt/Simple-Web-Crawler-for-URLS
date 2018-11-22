# Simple Web Crawler
## Returns N unique urls from the given start url

This simple webcrawler uses pythons requests library to scrape the data from the given url. BeautifulSoup4 is used to parse the raw HTML for <a\> tags. It then loops through each tag looking for links in the href section of the tag.

It adds the urls to a set. This ensures that all the urls gathered are unique as a set only allows one entry per element.

The program starts with the inputted start url. If this page does not contain N links it will use a url that it has found to continue looking. When the set is filled to the specified number (N) it will return and print the list of unique urls.

## Usage
I suggest using virtualenv for this

1. Create a virtualenv with python3 and activate it
2. Install requirements by running
```bash
pip install -r requirements.txt
```
3. Run the program by running. The program defaults to run with N = 100 and the start url = "https://www.bbc.com"
```bash
python webCrawler.py
```
4. Specify N and the start url with -n and -url. You can get the help page by running
```bash
python webCrawler.py -h
```
