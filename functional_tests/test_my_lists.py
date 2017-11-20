from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_preauthenticated_session


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_saved_as_my_lists(self):
        # Bob is a logged-in user
        self.create_preauthenticated_session('bob@example.com')

        # He goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # He notices a "My List" link for the first time
        self.browser.find_element_by_link_text('My lists').click()

        # He sees that his list is in there, named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # He decides to test out the awesome new private list functionality
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under "My lists", his new list appears!
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # He logs out. The "My lists" option disappears.
        self.browser.find_element_by_link_text('Log out').click()
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn('My lists', navbar.text)
