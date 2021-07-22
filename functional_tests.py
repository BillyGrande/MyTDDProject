from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_late(self):

        # Nikos Mexas wants to to-do his new life
        # He visits the url Billy suggested him earlier this day
        self.browser.get('http://localhost:8000')

        # He notices the page title and misses header bcs he stupid.
        # Both mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # He is encouraged to enter a to-do item straight away

        # He types "Meet my friend Odysseas 8pm" (Don't forget Mexas is very social)

        # He hits enter with his clumsy fingers, the page updates and now the page lists
        # "1: Meet my friend Ody at 8pm"

        # There is still a text box inviting him to add more items. He
        # enters "Cook lemonpie to bring Ody" (Nikos is a chef)

        # The page updates again, now both items are listed

        # Nikos wonders why his lemonpies sucks and wether the site will remember his list. Then he sees
        # that the site has generated a uniqued URL for him -- there is some
        # explanatory text to that effect

        # He visits that URL (big brain moment for Nikos) -
        # his to-do list is still there (yay!)

        # Satisfied, he cries himself to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')
