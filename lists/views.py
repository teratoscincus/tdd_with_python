from django.shortcuts import render, redirect

from .models import ListItem


def index(request):
    if request.method == "POST":
        ListItem.objects.create(text=request.POST.get("item_text", ""))
        return redirect("/lists/the-only-list-in-the-world/")
    return render(request, "lists/index.html")


def view_list(request):
    return render(
        request,
        "lists/list.html",
        context={
            "list_items": ListItem.objects.all(),
        },
    )
