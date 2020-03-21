from django.urls import path
from user.view import *
app_name = 'user'

urlpatterns = [
    path('register', user_register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('zhuce', user_zhuce, name='zhuce')
]