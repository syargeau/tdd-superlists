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
    Returns the list with associated items and allows posting new items.
    """
    # TODO: refactor out validation logic
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': list_, 'error': error})


def new_list(request):
    """
    Handles posts for new lists.
    """
    # TODO: refactor out hard-coded URL
    # TODO: refactor out validation logic
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
