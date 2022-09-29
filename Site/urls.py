from django.urls import path, include
from Site.views import *

urlpatterns = [
    path('',         Home,   name = 'home'),
    path('login',    Login,  name='login'),
    path('register', Register, name='register'),
    path('logout',    Logout,  name='logout'),
    path('private/',  include([
        path('',    private, name='private'), 
        path('tg-site/<int:id>',  TGSite, name='target-site'),
        path('history',  TGS_History),
        path('graph',    TGS_Graph), 
        path('graph/api',    TGS_graph_api), 
        path('relevee/', include([
            path('<int:siteid>',    Releve, name='relevee'), 
            path('scrap/start/<int:siteid>', Scrapper)
        ]))
    ])),
]
