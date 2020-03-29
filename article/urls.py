from django.conf.urls.static import static
from django.urls import path
from article.views import *
from dJan import settings

app_name = 'article'

urlpatterns = [
    path('detail', article_detail, name='detail'),
    path('show', article_show, name='show'),
    path('write', write_article, name='write'),
    path('comment', article_comment, name='comment')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 没有这一句无法显示上传的图片
