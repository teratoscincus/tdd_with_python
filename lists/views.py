from django.shortcuts import render, redirect

from .models import ListItem, List


def index(request):
    return render(request, "lists/index.html")


def view_list(request, pk):
    return render(
        request,
        "lists/list.html",
        context={
            "list": List.objects.get(pk=pk),
            "list_items": ListItem.objects.filter(list__pk=pk),
        },
    )


def new_list(request):
    list_ = List.objects.create()
    ListItem.objects.create(text=request.POST.get("item_text", ""), list=list_)
    return redirect(f"/lists/{list_.pk}/")


def add_item(request, pk):
    list_ = List.objects.get(pk=pk)
    ListItem.objects.create(text=request.POST.get("item_text", ""), list=list_)
    return redirect(f"/lists/{list_.pk}/")
