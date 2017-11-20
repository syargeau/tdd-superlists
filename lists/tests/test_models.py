from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from lists.models import Item, List

User = get_user_model()


class ItemModelTest(TestCase):
    """
    Tests Item model database functionality.
    """

    def test_default_text(self):
        """
        Test that the default text is a blank string.
        """
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        """
        Test that an item is linked to it's proper list.
        """
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_list_ordering(self):
        """
        Test that list items are ordered in the same order that they were entered.
        """
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self):
        """
        Test that items are represented as strings instead of the default object.
        """
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

    def test_cannot_save_empty_list(self):
        """
        Test that an empty item can't be passed into the list
        """
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
    def test_duplicate_items_are_invalid(self):
        """
        Test that duplicate items are invalid at the model level.
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        """
        Test that the same item can be saved to different lists.
        """
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # no error should be raised

    
class ListModelTest(TestCase):
    """
    Test that the List Model works as expected.
    """

    def test_get_absolute_url(self):
        """
        Test that the URL used is the one we want.
        """
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

<<<<<<< HEAD
    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owners(self):
        List(owner=User())  # should not raise

    def test_list_owner_is_optional(self):
        List().full_clean()  # should not raise

    def test_create_returns_new_list_object(self):
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_text(self):
=======
    def test_lists_can_have_owners(self):
        owner = User.objects.create(email='a@b.com')
        list_ = List.objects.create(owner=owner)
        self.assertIn(list_, owner.list_set.all())

    def test_list_owner_is_optional(self):
        List.objects.create()  # should not raise

    def test_list_name_is_first_item(self):
>>>>>>> bdf251d556751528bfd66b7fdbed885248ba720d
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')
