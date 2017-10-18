from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
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
    # TODO: refactor out hard-coded URL
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:  # occurs when item is empty
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    """
    Handles posts for items added to existing lists.
    """
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
