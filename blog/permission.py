from rest_framework import permissions

# 添加特定动作的权限
class IsLoggedInUserOrAdmin(permissions.BasePermission):
    """验证请求的用户是否是本人或是管理员"""
    def has_object_permission(self, request, view, obj):
        print("$$: ", request.user, obj)
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):
    """has_permission在刚开始判断请求的时候调用, has_object_permission在get_object的时候调用"""
    def has_permission(self, request, view):
        print(request.user)
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        print(request.user)
        return request.user and request.user.is_staff

class NoPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return False

    def has_permission(self, request, view):
        return False

class IsOwnArticle(permissions.BasePermission):
    """检查创建文章的作者是否是本人"""
    def has_object_permission(self, request, view, obj):
        """只设置has_object_permission，创建不需要访问对象"""
        print(request.user)
        return obj.user == request.user or request.user.is_staff