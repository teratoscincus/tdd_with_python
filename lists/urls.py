from django.urls import path, re_path

from .views import index, view_list, new_list

app_name = "lists"
urlpatterns = [
    path("", index, name="index"),
    re_path(r"^lists/the-only-list-in-the-world/$", view_list, name="view_list"),
    re_path(r"^lists/new$", new_list, name="new_list"),
]
