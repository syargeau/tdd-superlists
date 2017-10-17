from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """
    Test that items are verified properly.
    """

    def test_cannot_add_empty_list_items(self):
        """
        Test that blank lines cannot be submitted to the list.
        """
        # Bob goes to the home page and accidentally enters a blank item
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, but there's an error stating items cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # He tries again with a text item, which now works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. Buy milk')

        # To test, he attempts to submit another blank item to the list
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # Again, he recieves a warning that is not valid
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # And he can correct it by filling some text in
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. Buy milk')
        self.wait_for_item_in_list('2. Make tea')
