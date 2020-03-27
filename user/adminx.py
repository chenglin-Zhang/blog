import xadmin

# Register your models here.
from article.models import Article, Tag
from user.models import UserProfiles

# 在使用admin的时候已经默认添加了用户表
# xadmin.site.register(UserProfiles)
from xadmin import views


class BaseSettings(object):
    # 设置主题
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 设置LOGO
    site_title = '后台管理系统'
    # 设置页脚 @
    site_footer = '呈林の博客'


# 注册自定义设置
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
