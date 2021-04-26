from django.contrib import admin
from .models import *

# 控制admin界面数据的显示形式
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['id', 'username', 'email']

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'username']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Avatar)