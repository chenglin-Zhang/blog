from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from article.forms import ArticleForm
from article.models import Article, Tag, Comment, Message


def index(request):
    articles = Article.objects.all().order_by("-click_num")[:3]
    darticles = Article.objects.all().order_by("-data")[:8]
    # print(darticles)
    # print(articles)
    return render(request, 'index.html', context={"articles": articles, "darticles": darticles})


# 文章详情
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
            if article1 not in list_about and len(list_about) <= 5 and article1.id != int(id):
                print("%s-----%s" % (id, article1.id))
                list_about.append(article1)

    # 查询评论数
    comments = Comment.objects.filter(article_id=id)
    return render(request, 'article/info.html', context={'article': article, 'list_about': list_about, "comments": comments})


# 文章展示
def article_show(request):
    tags = Tag.objects.all()[:6]
    tid = request.GET.get("tid", "")

    # tag 和 article表 联合查询
    if tid:
        tag = Tag.objects.get(pk=tid)
        articles = tag.article_set.all()
    else:
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


# 写博客
def write_article(request):
    if request.method == "GET":
        aform = ArticleForm()
        return render(request, 'article/write.html', context={'form': aform})
    else:
        aform = ArticleForm(request.POST, request.FILES)
        if aform.is_valid():
            print("校验通过")
            data = aform.cleaned_data
            article = Article()
            article.title = data.get('title')
            article.desc = data.get('desc')
            article.content = data.get('content')
            print(type(data.get('image')))

            article.image = data.get('image')
            article.desc = data.get('desc')
            article.user = request.user  # 1对多 直接赋值
            article.save()
            # 多对多 必须添加到文章保存的后面添加
            article.tags.set(data.get('tags'))
            # return render(redirect('index'))
            return redirect(reverse('index'))
        else:
            print("校验不通过")
            return render(request, 'article/write.html', context={'form': aform})


# 文章评论
def article_comment(request):
    nickname = request.GET.get("nickname")
    saytext = request.GET.get("saytext")
    aid = request.GET.get("aid")

    comment = Comment.objects.create(nickname=nickname, content=saytext, article_id=aid)
    if comment:
        data = {'status': 1}
    else:
        data = {'status': 0}
    return JsonResponse(data)


# 文章留言
def blog_message(request):
    messages = Message.objects.all()
    paginator = Paginator(messages, 8)
    # 获取页码数
    page = request.GET.get('page', 1)
    # 得到page对象
    page = paginator.get_page(page)
    if request.method == "GET":
        return render(request, 'article/lmessage.html', {'page': page})
    else:
        name = request.POST.get('name')
        mycall = request.POST.get('mycall')
        lytext = request.POST.get('lytext')
        if name and lytext:
            message = Message.objects.create(nickname=name, content=lytext, icon=mycall)
            if message:
                return redirect(reverse("article:message"))
        return render(request, 'article/lmessage.html', context={"page": page, 'error':'必须输入用户名和内容'})