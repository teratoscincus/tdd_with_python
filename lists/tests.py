from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from . import views


class HomePageTest(TestCase):
    def test_root_url_resolve_to_index_view(self):
        found = resolve("/")
        self.assertEqual(found.func, views.index)

    def test_index_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.index(request)
        expected_html = render_to_string("lists/index.html")
        self.assertEqual(response.content.decode(), expected_html)
