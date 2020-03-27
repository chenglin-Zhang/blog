from django.contrib import admin

# Register your models here.
import article
from article.models import Article, Tag
from user.models import UserProfiles

admin.site.register(UserProfiles)
