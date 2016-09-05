from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class FunctionalTest(LiveServerTestCase):
    def setUp(self):
        # User Chrome as its the mostly used browser
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_numbers_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_basic_functionality_of_boilerplate(self):
        self.browser.get(self.live_server_url)

        # Make sure the title has the app name
        self.assertIn('Fibonacci Numbers', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Fibonacci Numbers', header_text)

        # There should be a input tag to enter 'N'
        inputbox = self.browser.find_element_by_id('id_new_n')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Enter 'N'")

        # Hitting Enter should make a POST request to get the Nth
        # number and display it on page
        inputbox.send_keys(6)
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_table('8')