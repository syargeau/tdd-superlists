from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_list_with_another_user(self):
        # Bob is logged in as a user
        self.create_preauthenticated_session('bob@example.com')
        bob_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(bob_browser))

        # Bob's friend Tom is also hanging out on the rad new site
        tom_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(tom_browser))
        self.browser = tom_browser
        self.create_preauthenticated_session('tom@example.com')

        # Bob goes to the home page and starts a list
        self.browser = bob_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')

        # He notices a "Share this list" option
        share_box = self.browser.find_element_by_css_selector('input[name="sharee"]')
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.complex'
        )
