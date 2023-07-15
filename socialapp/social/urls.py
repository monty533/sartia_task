from django.urls import path
from .views import *

app_name = 'social'

urlpatterns = [
    path('',index,name='index'),
    path('login/',LoginUser.as_view(),name='login'),
    path('register/',RegisterUser.as_view(),name='register'),
    path('logout/',logout_user,name='logout'),
    path('chat/<int:pk>/<str:name>',chatting,name='chatting')
]