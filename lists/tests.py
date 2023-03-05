from django.test import TestCase
from django.urls import resolve

from . import views


class HomePageTest(TestCase):
    def test_root_url_resolve_to_index_view(self):
        found = resolve("/")
        self.assertEqual(found.func, views.index)
