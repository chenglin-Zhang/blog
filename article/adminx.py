import xadmin

# Register your models here.
from article.models import Article, Tag

class ArticleAdmin(object):
    # Article表中展示的列
    list_display = ["title", 'desc', 'data', 'click_num']
    # 搜索: 根据字段模糊查询
    search_fields = ['id', 'title']
    # 修改: 在页面上直接修改
    list_editable = ['click_num']
    # 过滤: 根据字段进行过滤
    list_filter = ['data', 'user']



xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag)