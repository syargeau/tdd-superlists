from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth import get_user_model
from lists.models import Item, List
from lists.forms import (
    ItemForm, ExistingListItemForm,
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
)

User = get_user_model()


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

    def test_home_uses_item_form(self):
        """
        Test that the home page uses the item form for creating new list items.
        """
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    """
    Tests our list views.
    """

    def test_uses_list_template(self):
        """
        Test that the list view uses the list template.
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_items_for_list(self):
        """
        Test that all items for that list only are displayed.
        """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_correct_list_for_template(self):
        """
        Test that the correct list is used in the template.
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_save_post_request_to_existing_list(self):
        """
        Test that we can save a post request with item to an existing list.
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_post_redirect_to_list_view(self):
        """
        Test that a post to an existing list gets redirected to the correct list view.
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_displays_item_form(self):
        """
        Test that list views use the Item form we want.
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        """
        Return a post reponse of posting an empty item to a list.
        """
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text': ''})

    def test_invalid_input_not_in_db(self):
        """
        Tests that posting an invalid input doesn't save it to the database.
        """
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_list_template(self):
        """
        Tests that posting an invalid input renders the list view.
        """
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_invalid_input_passes_form_to_template(self):
        """
        Tests that posting an invalid input passes the correct form to the rendered template.
        """
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_input_shows_error(self):
        """
        Tests that posting an invalid input shows the correct error message.
        """
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_shows_error(self):
        """
        Test that when a duplicate item is entered, the list view shows the error message.
        """
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class NewListTest(TestCase):
    """
    Test the ability to add new lists.
    """

    def test_save_post_request(self):
        """
        Tests that a post request gets saved in database.
        """
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_post(self):
        """
        Tests that a post is redirected to the proper list URL.
        """
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_invalid_input_renders_home_page(self):
        """
        Tests that inputs with empty items are redirected back to the home page.
        """
        # TODO: refactor out hard-coded URLs
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_error_on_home_page(self):
        """
        Tests that if an empty item is submitted, the correct error message is shown.
        """
        # TODO: refactor out hard-coded URLs
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_invalid_input_passes_form_to_template(self):
        """
        Tests that an invalid input passes the input form back to the template.
        """
        # TODO: refactor out hard-coded URLs
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        """
        Tests that empty items are saved to the database.
        """
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class MyListsTest(TestCase):

    def test_my_lists_url_renders_correct_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)
