from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """只有本人才能进行的操作"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

class IsOwnerOrAdmin(BasePermission):
    """只有本人或者管理员或文章所有者才能进行的操作"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_superuser or request.user.id == obj.article.user_id

