from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

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

    def test_home_with_correct_html(self):
        """
        Tests that the home page has the correct html included.
        """
        request = HttpRequest
        reponse = home_page(request)
        html = reponse.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.endswith("</html>"))
