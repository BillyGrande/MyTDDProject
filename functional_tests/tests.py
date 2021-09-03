from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):


    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):

        # Nikos Mexas wants to to-do his new life
        # He visits the url Billy suggested him earlier this day
        self.browser.get(self.live_server_url)

        # He notices the page title and misses header bcs he stupid.
        # Both mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is encouraged to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Meet my friend Odysseas at 8pm" (Don't forget Mexas is very social)
        inputbox.send_keys('Meet my friend Ody at 8pm')

        # He hits enter with his clumsy fingers, the page updates and now the page lists
        # "1: Meet my friend Ody at 8pm"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Meet my friend Ody at 8pm')

        # There is still a text box inviting him to add more items. He
        # enters "Cook lemonpie to bring Ody" (Nikos is a chef)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Cook lemonpie to bring Ody')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, now both items are listed
        self.wait_for_row_in_list_table('1: Meet my friend Ody at 8pm')
        self.wait_for_row_in_list_table('2: Cook lemonpie to bring Ody')


        # Nikos wonders why his lemonpies sucks and wether the site will remember his list. Then he sees
        # that the site has generated a uniqued URL for him -- there is some
        # explanatory text to that effect

        # He visits that URL (big brain moment for Nikos) -
        # his to-do list is still there (yay!)

        # Satisfied, he cries himself to sleep


    def test_multiple_users_can_start_lists_at_different_urls(self):

        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #She notices that her list has a unique url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        #Satisfied, the both go back to sleep

    def test_layout_and_styling(self):

        #Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        #She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] +  inputbox.size['width'] / 2,
            512,
            delta = 10
        )
