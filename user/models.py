from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfiles(AbstractUser):
    # 添加字段
    mobile = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d', default='uploads/minel.png')

    class Meta:
        db_table = 'userprofile'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
