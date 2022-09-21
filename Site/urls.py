from django.contrib import admin
from django.urls import path
from Site import views # Dois être importer manuellement en fonction de l'app

urlpatterns = [
    path('',         views.HomePage, name = 'home'),
    # path('contact',  views.contact, name="contact"),
    # path('login',    views.login, name='login'),
    # path('register', views.registration, name='register'),
]
