from django.urls import path
from user.view import *
app_name = 'user'

urlpatterns = [
    path('register', user_register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('codelogin', code_login, name='codelogin'),
    path('send_code', send_code, name='send_code'),
    path('zhuce', user_zhuce, name='zhuce')
]