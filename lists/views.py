from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    """
    Returns the desired home page upon http request.
    """
    return render(request, 'home.html')


def view_list(request, list_id):
    """
    Returns the list with associated items.
    """
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """
    Handles posts for new lists.
    """
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    """
    Handles posts for items added to existing lists.
    """
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
