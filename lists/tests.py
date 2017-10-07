from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):
    """
    Tests our home page functionality.
    """

    def test_root_url_returns_home_view(self):
        """
        Tests that root url successfully resolves to home page view.
        """
        found = resolve("/")
        self.assertEqual(found.func, home_page)
