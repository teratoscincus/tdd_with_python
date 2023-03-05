from django.urls import path

from .views import index

app_name = "lists"
urlpatterns = [
    path("", index, name="index"),
]
