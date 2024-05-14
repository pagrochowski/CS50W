import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

class WebpageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless=new") 
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu") 
        options.binary_location = '/usr/bin/chromium-browser' 

        service = Service()
        cls.driver = webdriver.Chrome(service=service, options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_title(self):
        """Make sure title is correct"""
        self.driver.get(file_uri("counter.html"))
        self.assertEqual(self.driver.title, "Counter")

    def test_increase(self):
        """Make sure header updated to 1 after 1 click of increase button"""
        self.driver.get(file_uri("counter.html"))
        increase = self.driver.find_element("id", "increase")
        increase.click()
        self.assertEqual(self.driver.find_element("tag name", "h1").text, "1")

    def test_decrease(self):
        """Make sure header updated to -1 after 1 click of decrease button"""
        self.driver.get(file_uri("counter.html"))
        decrease = self.driver.find_element("id", "decrease")
        decrease.click()
        self.assertEqual(self.driver.find_element("tag name", "h1").text, "-1")

    def test_multiple_increase(self):
        """Make sure header updated to 3 after 3 clicks of increase button"""
        self.driver.get(file_uri("counter.html"))
        increase = self.driver.find_element("id", "increase")
        for i in range(3):
            increase.click()
        self.assertEqual(self.driver.find_element("tag name", "h1").text, "3")


if __name__ == "__main__":
    unittest.main()
