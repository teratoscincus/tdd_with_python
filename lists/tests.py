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

    def test_index_page_can_save_a_POST_request(self):
        # Setup
        request = HttpRequest()
        request.method = "POST"
        item_text = "A new list item"
        request.POST["item_text"] = item_text
        # Exercise
        response = views.index(request)
        # Assert
        self.assertEqual(ListItem.objects.count(), 1)
        new_item = ListItem.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_index_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = "POST"
        item_text = "A new list item"
        request.POST["item_text"] = item_text

        response = views.index(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_index_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        views.index(request)
        self.assertEqual(ListItem.objects.count(), 0)


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
