from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


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
