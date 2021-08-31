from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_late(self):

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
        time.sleep(1)
        self.check_for_row_in_list_table('1: Meet my friend Ody at 8pm')

        # There is still a text box inviting him to add more items. He
        # enters "Cook lemonpie to bring Ody" (Nikos is a chef)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Cook lemonpie to bring Ody')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, now both items are listed
        self.check_for_row_in_list_table('1: Meet my friend Ody at 8pm')
        self.check_for_row_in_list_table('2: Cook lemonpie to bring Ody')


        # Nikos wonders why his lemonpies sucks and wether the site will remember his list. Then he sees
        # that the site has generated a uniqued URL for him -- there is some
        # explanatory text to that effect
        self.fail('Finisth the test!')

        # He visits that URL (big brain moment for Nikos) -
        # his to-do list is still there (yay!)

        # Satisfied, he cries himself to sleep

