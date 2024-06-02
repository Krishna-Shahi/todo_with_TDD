from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        myList = List()
        myList.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = myList
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = myList
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, myList)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, myList)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, myList)

    def test_cannot_save_empty_list_items(self):
        mylist = List.objects.create()
        item = Item(list=mylist, text="")
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()
            
    def test_get_absolute_url(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f"/lists/{mylist.id}/")        