from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    """
    Returns the desired home page upon http request.
    """
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list')
    return render(request, 'home.html')


def view_list(request):
    """
    Returns the list.
    """
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
