from django.urls import path

from .views import view_list, new_list, add_item

app_name = "lists"
urlpatterns = [
    path("<int:pk>/", view_list, name="view_list"),
    path("<int:pk>/add-item", add_item, name="add_item"),
    path("new", new_list, name="new_list"),
]
