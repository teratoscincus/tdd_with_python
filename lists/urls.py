from django.urls import path, re_path

from .views import index, view_list

app_name = "lists"
urlpatterns = [
    path("", index, name="index"),
    re_path(r"^lists/the-only-list-in-the-world/$", view_list, name="view_list"),
]
