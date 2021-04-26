from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsOwner, IsOwnerOrAdmin


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
    def get_permissions(self):
        """设置评论功能的权限"""
        # get和list对所有用户包括游客放行
        print('cuk:', self.action)
        permission_classes = []
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        # update只对本人放行
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwner]
        # delete只对本人和管理员放行
        elif self.action == 'destroy':
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

