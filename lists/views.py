from django.shortcuts import render

def home_page(request):
    reponse = render(request, 'home.html')
    return reponse
