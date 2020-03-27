from django.shortcuts import render

# Create your views here.
from article.models import Article


def index(request):
    articles = Article.objects.all().order_by("-click_num")[:3]
    print(articles)
    return render(request, 'index.html', context={"articles": articles})
