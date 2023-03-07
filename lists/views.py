from django.shortcuts import render, redirect

from .models import ListItem


def index(request):
    if request.method == "POST":
        ListItem.objects.create(text=request.POST.get("item_text", ""))
        return redirect("/")

    return render(
        request,
        "lists/index.html",
        context={
            "list_items": ListItem.objects.all(),
        },
    )
