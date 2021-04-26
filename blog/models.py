from django.db import models
from django.utils import timezone
from markdown import Markdown
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Avatar(models.Model):
    value = models.ImageField(upload_to='photos/%Y%m%d', default="avatar.jpg")

class User(AbstractUser):
    # email字段用于验证不能重复，技术上来说username可以重复，但是一般习惯用单一username
    username = models.CharField(max_length=30, blank=False, default="", unique=True)
    email = models.EmailField(max_length=50, unique=True, null=False)

    # 权限管理中，如果请求需要有用户的身份需要输入相应的username和password
    # 指定username实际检查的字段
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.email)

    class Meta:
        ordering = ['-id']

class UserProfile(models.Model):
    # related_name用于对应表调用本表对象所使用的属性名
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile',
                                null=True, blank=True)
    intro = models.CharField(max_length=50, default="", blank=True)
    registered = models.DateField(auto_now=True)
    country = models.CharField(max_length=50, default="", blank=True)
    city = models.CharField(max_length=50, default="", blank=True)
    zip = models.CharField(max_length=20, default='', blank=True)
    address = models.CharField(max_length=50, default="", blank=True)
    photo = models.OneToOneField(to='Avatar', blank=True, null=True, related_name='userprofile',
                                    on_delete=models.CASCADE)
    class Meta:
        ordering = ['-id']


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=80, default="未命名")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(to='Tag', related_name='articles')
    read_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    like_persons = models.ManyToManyField(to='User', related_name='like_articles', blank=True)
    def getMd(self):
        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        htmlbody = md.convert(self.body)
        return htmlbody, md.toc
    class Meta:
        ordering = ['-id']

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']      # 数据按照id降序排列



