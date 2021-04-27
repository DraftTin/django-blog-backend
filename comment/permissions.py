from rest_framework.permissions import BasePermission
from .models import Comment

class IsOwner(BasePermission):
    """只有本人才能进行的操作"""
    def has_object_permission(self, request, view, obj):
        print(request.data)
        return request.user == obj.user

class IsOwnerOrAdmin(BasePermission):
    """只有本人或者管理员或文章所有者才能进行的操作"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_superuser or request.user.id == obj.article.user_id

class OnlyUpdateContent(BasePermission):
    """更新评论只能更改评论的content，其他种类的更新均不允许"""
    def has_object_permission(self, request, view, obj):
        if 'content' in request.data.keys() and len(request.data.keys()) == 1:
            return True
        return False

class OnlyCreateOwnComment(BasePermission):
    """只能创建user为自己的评论"""
    def has_permission(self, request, view):
        if 'user_id' in request.data.keys():
            user_id = int(request.data['user_id'])
            return user_id == request.user.id
        return True

class OnlyFromSameArticle(BasePermission):
    """创建评论的时候只能回复同一文章的其他评论"""
    def has_permission(self, request, view):
        if 'quote_comment_id' in request.data.keys() and request.data['quote_comment_id'] != None\
                and 'article_id' in request.data.keys():
            print(request.data)
            article_id = int(request.data['article_id'])
            quote_comment_id = int(request.data['quote_comment_id'])
            print(article_id, Comment.objects.get(pk=quote_comment_id).article_id)
            return article_id == Comment.objects.get(pk=quote_comment_id).article_id
        return True