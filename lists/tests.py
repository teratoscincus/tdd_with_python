import re

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from . import views
from .models import ListItem, List


class HomePageTest(TestCase):
    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r"<input[^>]+csrfmiddlewaretoken[^>]+>"
        return re.sub(csrf_regex, "", html_code)

    def assertHTMLEqualExceptCSRF(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1), self.remove_csrf(html_code2)
        )

    def test_root_url_resolve_to_index_view(self):
        found = resolve("/")
        self.assertEqual(found.func, views.index)

    def test_index_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.index(request)
        expected_html = render_to_string("lists/index.html")
        self.assertHTMLEqualExceptCSRF(response.content.decode(), expected_html)


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(ListItem.objects.count(), 1)
        new_item = ListItem.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], f"/lists/{new_list.pk}/")
        self.assertRedirects(response, f"/lists/{new_list.pk}/")


class NewListItemTest(TestCase):
    def test_can_save_a_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.pk}/add-item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(ListItem.objects.count(), 1)
        new_item = ListItem.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.pk}/add-item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.pk}/")


class ListAndItemModelsIntegratedTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = ListItem()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = ListItem()
        second_item.text = "The second item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = ListItem.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "The second item")
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.pk}/")
        self.assertTemplateUsed(response, "lists/list.html")

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        ListItem.objects.create(text="Item 1", list=correct_list)
        ListItem.objects.create(text="Item 2", list=correct_list)
        other_list = List.objects.create()
        ListItem.objects.create(text="Other list item 1", list=other_list)
        ListItem.objects.create(text="Other list item 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.pk}/")

        self.assertContains(response, "Item 1")
        self.assertContains(response, "Item 2")
        self.assertNotContains(response, "Other list item 1")
        self.assertNotContains(response, "Other list item 2")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.pk}/")
        self.assertEqual(response.context["list"], correct_list)
