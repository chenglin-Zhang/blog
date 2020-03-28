from django.urls import path
from article.views import *

app_name = 'article'

urlpatterns = [
    path('detail', article_detail, name='detail'),
    path('show', article_show, name='show')
]
