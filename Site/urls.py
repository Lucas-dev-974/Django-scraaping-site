from django.contrib import admin
from django.urls import path, include
from Site.views import *

urlpatterns = [
    path('',         Home,   name = 'home'),
    path('login',    Login,  name='login'),
    path('register', Register, name='register'),
    path('tg-site/',  include([
        path('',         TGSite, name='target-site'),
        path('history',  TGS_History),
        path('graph',    TGS_Graph) 
    ])),
]
