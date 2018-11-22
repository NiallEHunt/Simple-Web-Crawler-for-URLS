import subprocess
import unittest

class TestWebCrawlerDuplicates(unittest.TestCase):
    def test_for_duplicates_bbc(self):
        output = subprocess.check_output(["python", "webCrawler.py"])
        links = output.splitlines()
        self.assertEqual(len(links), len(set(links)), "Length of links outputted should equal the length of the set of the outputted list. (ie. should be no duplicates)")

    def test_for_duplicates_small_site(self):
        output = subprocess.check_output(["python", "webCrawler.py", "-url", "https://www.scss.tcd.ie/John.Waldron/3071/3071.html"])
        links = output.splitlines()
        self.assertEqual(len(links), len(set(links)), "Length of links outputted should equal the length of the set of the outputted list. (ie. should be no duplicates)")

    def test_for_duplicates_site_with_no_links(self):
        output = subprocess.check_output(["python", "webCrawler.py", "-url", "https://www.ghacks.net/wp-content/uploads/2007/03/encrypt-url.jpg"])
        links = output.splitlines()
        self.assertEqual(len(links), len(set(links)), "Length of links outputted should equal the length of the set of the outputted list. (ie. should be no duplicates)")

class TestWebCrawlerNLinks(unittest.TestCase):
    def test_for_100_links_bbc(self):
        output = subprocess.check_output(["python", "webCrawler.py"])
        links = output.splitlines()
        self.assertEqual(len(links), 100, "Length of links should equal N (default is 100)")

    def test_for_500_links_bbc(self):
        output = subprocess.check_output(["python", "webCrawler.py", "-n", "500"])
        links = output.splitlines()
        self.assertEqual(len(links), 500, "Length of links should equal 500")

    def test_for_100_small_site(self):
        output = subprocess.check_output(["python", "webCrawler.py", "-url", "https://www.scss.tcd.ie/John.Waldron/3071/3071.html"])
        links = output.splitlines()
        self.assertLess(len(links), 100, "Length of links should be less than N as site crawling from this start won't find 100 links")

    def test_for_100_no_links_site(self):
        output = subprocess.check_output(["python", "webCrawler.py", "-url", "https://www.ghacks.net/wp-content/uploads/2007/03/encrypt-url.jpg"])
        links = output.splitlines()
        self.assertLess(len(links), 100, "Length of links should be less than N as site crawling from this start won't find 100 links")

class TestWebCrawlerIncorrectURL(unittest.TestCase):
    def test_for_incorrect_url(self):
        output = subprocess.check_output(["python", "webCrawler.py", "-url", "fake.url.for/testing"])
        links = output.splitlines()
        strings = []
        for link in links:
            strings.append(str(link))
        self.assertIn("b'Invalid url'", strings)
