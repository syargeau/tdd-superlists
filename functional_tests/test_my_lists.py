from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_preauthenticated_session


class MyListsTest(FunctionalTest):

    def create_preauthenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_preauthenticated_session(email)
        ## to set a cookie we first need to visit the domain
        ## 404 pages load the quickest
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path='/'
            )
        )
    
    def test_logged_in_users_lists_saved_as_my_lists(self):
        email = 'bob@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Bob is a logged-in user
        self.create_preauthenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
