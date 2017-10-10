from django.test import TestCase

from lists.models import Item


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


class ItemModelTest(TestCase):
    """
    Tests database functionality.
    """

    def test_save_and_load(self):
        """
        Tests ability to save to and load from the database.
        """
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'The second list item')


class ListViewTest(TestCase):
    """
    Tests our list views.
    """

    def test_uses_list_template(self):
        """
        Test that the list view uses the list template.
        """
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items(self):
        """
        Test that all list items are displayed.
        """
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        response = self.client.get('/lists/the-only-list/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):
    """
    Test the ability to add new lists.
    """

    def test_save_post_request(self):
        """
        Tests that a post request gets saved in database.
        """
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_post(self):
        """
        Tests that a post is redirected to the proper list URL.
        """
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list/')
