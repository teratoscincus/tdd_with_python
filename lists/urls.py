from django.urls import path, re_path

from .views import index, view_list, new_list, add_item

app_name = "lists"
urlpatterns = [
    path("", index, name="index"),
    path("lists/<int:pk>/", view_list, name="view_list"),
    path("lists/<int:pk>/add-item", add_item, name="add_item"),
    re_path(r"^lists/new$", new_list, name="new_list"),
]
