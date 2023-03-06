from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(
        request,
        "lists/index.html",
        context={"new_item_text": request.POST.get("item_text", "")},
    )
