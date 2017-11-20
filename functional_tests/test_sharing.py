from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


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
        list_page = ListPage(self).add_list_item('Get help')

        # He notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.complex'
        )

        # He shares his list. The page updates stating it was shared with Tom.
        list_page.share_list_with('tom@example.com')

        # Tom now goes to his list page
        self.browser = tom_browser
        MyListsPage(self).go_to_my_lists_page()

        # He sees Bob's list in there!
        self.browser.find_element_by_link_text('Get help').click()
        self.wait_for(
            lambda: self.assertEqual(
                list_page.get_list_owner(),
                'bob@example.com'
            )
        )

        # He adds an item to Bob's list
        list_page.add_list_item('Hi Bob!')

        # When Bob refreshes the page, he sees Tom's addition
        self.browser = bob_browser
        self.browser.refresh()
        list_page.wait_for_item_in_list('Hi Bob!', 2)
