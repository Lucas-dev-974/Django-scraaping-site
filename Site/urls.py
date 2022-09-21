from django.contrib import admin
from django.urls import path, include
from Site.viewpackage import *

urlpatterns = [
    path('',         HomePage,   name = 'home'),
    path('login',    LoginPage,  name='login'),
    path('register', RegisterPage, name='register'),
    path('tg-site/',  include([
        path('',         TGSitePage, name='target-site'),
        path('history',  TGS_HistoryPage),
        path('graph',    TGS_GraphPage)
    ])),
]
