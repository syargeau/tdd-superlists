from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStyling(FunctionalTest):
    """
    Test that the layout and styling is applied as expected.
    """

    def test_layout_and_styling(self):
        """
        Test that our CSS is being applied as expected.
        """
        # Bob goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta=10
        )

        # He starts a new list, and notices the input box is nicely centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list('1. testing')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta=10
        )
