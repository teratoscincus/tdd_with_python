from django.shortcuts import render, redirect

from .models import ListItem, List


def index(request):
    return render(request, "lists/index.html")


def view_list(request):
    return render(
        request,
        "lists/list.html",
        context={
            "list_items": ListItem.objects.all(),
        },
    )


def new_list(request):
    list_ = List.objects.create()
    ListItem.objects.create(text=request.POST.get("item_text", ""), list=list_)
    return redirect("/lists/the-only-list-in-the-world/")
