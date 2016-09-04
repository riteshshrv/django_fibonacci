import unittest
from selenium import webdriver

class FunctionalTest(unittest.TestCase):
    def setUp(self):
        # User Chrome as its the mostly used browser
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_boilerplate(self):
        self.browser.get('http://localhost:8000')

        # Make sure the title has the app name
        self.assertIn('Fibonacci Numbers', self.browser.title)

        # There should be a input tag to enter 'N'

        # Hitting Enter should make a POST request to get the Nth
        # number and display it on page


if __name__ == '__main__':
    unittest.main(verbosity=2)

