from django.shortcuts import render

# Create your views here.

def LoginPage(request):
    return render(request, 'template-parts/login.html')

def RegisterPage(request):
    return render(request, 'template-parts/register.html')
