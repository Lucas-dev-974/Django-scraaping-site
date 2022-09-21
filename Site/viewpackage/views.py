from django.shortcuts import render

from . import * 

# Create your views here.
def HomePage(request):
    return render(request, 'template-parts/home.html')

