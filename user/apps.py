from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    # 修改后台列表标题
    verbose_name = '用户操作'