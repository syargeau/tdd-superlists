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

        # The home page refreshes, but there's an error stating items cannot be blank

        # He tries again with a text item, which now works

        # To test, he attempts to submit another blank item to the list

        # Again, he recieves a warning that is not valid

        # And he can correct it by filling some text in
        self.fail('write me!')
