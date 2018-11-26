# I wasn't able to get the package structure to work for me so I'm just going to use this simple method instead
import sys
sys.path.append('../')
from fetch import find_links_on_page
import unittest
from unittest import mock

# Fake the requset response to use the test HTML documents
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text_data, status_code):
            self.text = text
            self.status_code = status_code

    if args[0] == 'http://large_site.com':
        with open('large_site.html') as f:
            text = f.read()
        return MockResponse(text, 200)
    elif args[0] == 'http://small_site.com':
        with open('small_site.html') as f:
            text = f.read()
        return MockResponse(text, 200)
    elif args[0] == 'http://single_page_site.com':
        with open('single_page_site.html') as f:
            text = f.read()
        return MockResponse(text, 200)
    elif args[0] == 'http://small_site_links_to_large.com':
        with open('small_site_links_to_large.html') as f:
            text = f.read()
        return MockResponse(text, 200)

    return MockResponse(None, 404)

class TestWebCrawlerNLinks(unittest.TestCase):
    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_for_100_links_large_site(self, mock_get):
        links = set()
        links = find_links_on_page('http://large_site.com', 100, links)
        self.assertEqual(len(links), 100, "Length of links should equal 100")

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_for_40_links_small_site(self, mock_get):
        links = set()
        links = find_links_on_page('http://small_site.com', 100, links)
        self.assertEqual(len(links), 40, "Length of links should equal 40")

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_for_no_links_single_page_site(self, mock_get):
        links = set()
        links = find_links_on_page('http://single_page_site.com', 100, links)
        self.assertEqual(len(links), 0, "Length of links should equal 0")

#     def test_for_500_links_bbc(self):
#         output = subprocess.check_output(["python", "webCrawler.py", "-n", "500"])
#         links = output.splitlines()
#         self.assertEqual(len(links), 500, "Length of links should equal 500")
#
#     def test_for_100_small_site(self):
#         output = subprocess.check_output(["python", "webCrawler.py", "-url", "https://www.scss.tcd.ie/John.Waldron/3071/3071.html"])
#         links = output.splitlines()
#         self.assertLess(len(links), 100, "Length of links should be less than N as site crawling from this start won't find 100 links")
#
#     def test_for_100_no_links_site(self):
#         output = subprocess.check_output(["python", "webCrawler.py", "-url", "https://www.ghacks.net/wp-content/uploads/2007/03/encrypt-url.jpg"])
#         links = output.splitlines()
#         self.assertLess(len(links), 100, "Length of links should be less than N as site crawling from this start won't find 100 links")
#
# class TestWebCrawlerIncorrectURL(unittest.TestCase):
#     def test_for_incorrect_url(self):
#         output = subprocess.check_output(["python", "webCrawler.py", "-url", "fake.url.for/testing"])
#         links = output.splitlines()
#         strings = []
#         for link in links:
#             strings.append(str(link))
#         self.assertIn("b'Invalid url'", strings)
#
#     def test_for_fake_url(self):
#         output = subprocess.check_output(["python", "webCrawler.py", "-url", "https://www.fake.site/testing"])
#         links = output.splitlines()
#         strings = []
#         for link in links:
#             strings.append(str(link))
#         self.assertIn("b'Invalid url'", strings)
