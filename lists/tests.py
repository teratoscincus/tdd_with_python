import re

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from . import views


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
        self.assertIn(item_text, response.content.decode())
        expected_html = render_to_string(
            "lists/index.html", context={"new_item_text": item_text}
        )
        self.assertHTMLEqualExceptCSRF(response.content.decode(), expected_html)
