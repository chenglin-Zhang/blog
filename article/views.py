from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from article.models import Article, Tag


def index(request):
    articles = Article.objects.all().order_by("-click_num")[:3]
    darticles = Article.objects.all().order_by("-data")[:8]
    # print(darticles)
    # print(articles)
    return render(request, 'index.html', context={"articles": articles, "darticles": darticles})


def article_detail(request):
    id = request.GET.get("id")
    article = Article.objects.get(pk=id)
    article.click_num += 1
    article.save()
    # 查询相关文章
    tags_list = article.tags.all()
    list_about = []
    for tag in tags_list:
        # 在article表中包含所有tag的内容
        for article1 in tag.article_set.all():
            # 列表中没有               and    列表条数不超过6    and      不包含自己
            if article1 not in list_about and len(list_about) <= 6 and article1.id != int(id):
                print("%s-----%s" % (id, article1.id))
                list_about.append(article1)
    return render(request, 'article/info.html', context={'article': article, 'list_about': list_about})


def article_show(request):
    tags = Tag.objects.all()[:6]
    tid = request.GET.get("tid")

    # tag 和 article表 联合查询
    if tid:
        tag = Tag.objects.get(pk=tid)
        articles = tag.article_set.all()
    else:
        tid = ''
        articles = Article.objects.all()

    paginator = Paginator(articles, 2)  # 分页对象 Paginator(列表对象, 每页个数)
    # print(paginator.count)  # 总的条数
    # print(paginator.num_pages)  # 总页数
    # print(paginator.page_range)  # 页码范围

    page = request.GET.get('page', 1)  # 默认第一页
    page = paginator.get_page(page)  # 返回page每页对象

    # page.has_next()  # 判断有没有下一页
    # page.has_previous()  # 判断有没有上一页
    # page.next_page_number()  # 返回下一页页码数
    # page.previous_page_number()  # 返回上一页页码数

    return render(request, 'article/learn.html', context={"tags": tags, "page": page, "tid": tid})
