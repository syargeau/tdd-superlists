from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import Item, List

User = get_user_model()


def home_page(request):
    """
    Returns the desired home page upon http request.
    """
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    """
    Returns the list with associated items and allows posting new items.
    """
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
<<<<<<< HEAD
        list_ = form.save(owner=request.user)
=======
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
>>>>>>> bdf251d556751528bfd66b7fdbed885248ba720d
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {"owner": owner})
