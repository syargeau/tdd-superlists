from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
    """
    Test expected outcomes for a new visitor.
    """
    
    def test_start_list_for_one_user(self):
        """
        Tests that a single user can start a list.
        """
        # Bob wants to check out our app. He goes to our homepage.
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do list right away.
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Call Mom and Dad".
        inputbox.send_keys('Call Mom and Dad')

        # When he hits enter, the page updates and the to-do list now states:
        # "1. Call Mom and Dad" as an item in the to-do list
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_item_in_list('1. Call Mom and Dad')

        # There is still a text box inviting him to enter another item. He enters "Call Brother".
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Call Brother')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items
        self.wait_for_item_in_list('1. Call Mom and Dad')
        self.wait_for_item_in_list('2. Call Brother')

        # Bob can now sleep peacefully, knowing he will remember to contact his family.

    def test_multiple_lists_with_specific_urls(self):
        """
        Test that multiple users can have their own lists, with each list having it's own URL.
        """
        # Bob starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Call Mom and Dad')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. Call Mom and Dad')

        # He notices that his list has a unique URL
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+')

        # Now, a new user, Sue, visits the site
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Sue vists the home page, and there is no sign of another list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Call Mom and Dad', page_text)
        self.assertNotIn('Call Brother', page_text)

        # Sue starts her own list
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy latest New Yorker')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. Buy latest New Yorker')

        # She gets her own unique URL
        sue_list_url = self.browser.current_url
        self.assertRegex(sue_list_url, '/lists/.+')
        self.assertNotEqual(sue_list_url, bob_list_url)

        # There is still no trace of Bob's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Call Mom and Dad', page_text)
        self.assertIn('Buy latest New Yorker', page_text)

        # Satisfied, they both go to sleep
