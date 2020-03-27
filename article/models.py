from django.db import models

# Create your models here.
from user.models import UserProfiles


class Tag(models.Model):
    '''
        JS Python Java ...
    '''
    name = models.CharField(max_length=50, verbose_name="标签")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    desc = models.CharField(max_length=256, verbose_name='简介')
    content = models.TextField(verbose_name='内容')
    data = models.DateField(auto_now=True, verbose_name='创建日期')
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    love_num = models.IntegerField(default=0, verbose_name='点赞量')
    image = models.ImageField(upload_to='uploads/article/%Y/%m/%d', verbose_name='文章封面')

    # 文章和标签多对多映射
    tags = models.ManyToManyField(to=Tag)
    #文章和用户多对一
    user = models.ForeignKey(to=UserProfiles, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = '文章表'
        verbose_name_plural = verbose_name