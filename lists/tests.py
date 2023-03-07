import re

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from . import views
from .models import ListItem


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
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/lists/the-only-list-in-the-world/")
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")


class ItemModelIntegratedTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = ListItem()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = ListItem()
        second_item.text = "The second item"
        second_item.save()

        saved_items = ListItem.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "The second item")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "lists/list.html")

    def test_displays_all_items(self):
        ListItem.objects.create(text="Item 1")
        ListItem.objects.create(text="Item 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "Item 1")
        self.assertContains(response, "Item 2")
