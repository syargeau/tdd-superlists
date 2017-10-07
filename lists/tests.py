from django.test import TestCase


class HomePageTest(TestCase):
    """
    Tests our home page functionality.
    """

    def test_uses_home_template(self):
        """
        Tests that the home page uses the correct html template.
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_save_post_request(self):
        """
        Tests that a post request gets submitted and saved successfully.
        """
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
