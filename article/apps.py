from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'article'
    # 修改后台列表标题
    verbose_name = '文章操作'