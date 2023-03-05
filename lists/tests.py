from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from . import views


class HomePageTest(TestCase):
    def test_root_url_resolve_to_index_view(self):
        found = resolve("/")
        self.assertEqual(found.func, views.index)

    def test_index_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.index(request)
        self.assertTrue(response.content.startswith(b"<html>"))
        self.assertIn(b"<title>To-Do lists</title>", response.content)
        self.assertTrue(response.content.endswith(b"</html>"))
