# I wasn't able to get the package structure to work for me so I'm just going to use this simple method instead
import sys
sys.path.append('../')
from io import TextIOWrapper, BytesIO
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

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_for_100_links_large_site(self, mock_get):
        links = set()
        links = find_links_on_page('http://small_site_links_to_large.com', 100, links)
        url = list(links)[0]
        links = find_links_on_page(url, 100, links)
        self.assertEqual(len(links), 100, "Length of links should equal 100")


class TestWebCrawlerIncorrectURL(unittest.TestCase):
    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_for_incorrect_url(self, mock_get):
        # Check the output of the program for the printing of 'Invalid url'
        # This is done by changing the stdout before running the function and checking
        # our new buffer for the string. We then restore stdout
        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        links = set()
        links = find_links_on_page("fake.path.test", 100, list)

        sys.stdout.seek(0)
        out = sys.stdout.read()

        sys.stdout.close()
        sys.stdout = old_stdout
        self.assertIn("Invalid url", out)

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_for_fake_url(self, mock_get):
        # Check the output of the program for the printing of 'Invalid url'
        # This is done by changing the stdout before running the function and checking
        # our new buffer for the string. We then restore stdout
        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        links = set()
        links = find_links_on_page("http://www.fake.com/Testing", 100, list)

        sys.stdout.seek(0)
        out = sys.stdout.read()

        sys.stdout.close()
        sys.stdout = old_stdout
        self.assertIn("Invalid url", out)
