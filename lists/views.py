from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    """
    Returns the desired home page upon http request.
    """
    return render(request, 'home.html')


def view_list(request):
    """
    Returns the list with associated items.
    """
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    """
    Handles posts for new lists.
    """
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list/')
