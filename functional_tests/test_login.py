from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'bob@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link(self):
        # Bob goes to the awesome Superlists site and notices a "login" section in the navbar
        # It's telling him to enter his email address, so he does
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling him an email was sent
        self.wait_for(
            lambda: self.assertIn(
                'Check your email',
                self.browser.find_element_by_tag_name('body').text
            )
        )

        # He checks his email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to login', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # He clicks it, and is logged in
        self.browser.get(url)
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Now he logs out
        self.browser.find_element_by_link_text('Log out').click()

        # He is logged out
        self.wait_to_be_logged_out(email=TEST_EMAIL)
