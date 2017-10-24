from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """
    Test that items are verified properly.
    """

    def get_error_element(self):
        """
        Return the error element.
        """
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        """
        Test that blank lines cannot be submitted to the list.
        """
        # Bob goes to the home page and accidentally enters a blank item
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts, and doesn't load the list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # He starts typing a text item, and the error disappers
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))

        # He can now successfully submit the text item
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. Buy milk')

        # To test, he attempts to submit another blank item to the list
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, he recieves a warning that is not valid
        self.wait_for_item_in_list('1. Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # And he can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. Buy milk')
        self.wait_for_item_in_list('2. Make tea')

    def test_cannot_add_duplicate_items(self):
        """
        Test that duplicate items can't be added to the same list
        """
        # Bob goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Call Papa')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. Call Papa')

        # He accidentally tries to enter the same item
        self.get_item_input_box().send_keys('Call Papa')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # He sees a helpful error message
        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text,
                "You've already got this item in your list"
            )
        )

    def test_error_messages_are_cleared_on_input(self):
        """
        Test that the error message for duplicates is cleared once text is entered in the form.
        """
        # Bob starts a list and causes a validation error
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Test duplicate error message disappers')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. Test duplicate error message disappers')
        self.get_item_input_box().send_keys('Test duplicate error message disappers')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertTrue(
                self.get_error_element().is_displayed()
            )
        )

        # He starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # He sees the error message disappear
        self.wait_for(
            lambda: self.assertFalse(
                self.get_error_element().is_displayed()
            )
        )
