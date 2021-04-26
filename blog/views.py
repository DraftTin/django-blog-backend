from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework_jwt.utils import jwt_decode_handler
# 引用自定义的权限
from .permission import *
from .models import *
from rest_framework import viewsets
from django.http import JsonResponse

# Create your views here.
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleDetailSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    def get_queryset(self):
        # 重写该方法使得获取
        searchText = self.request.query_params.get('searchText', None)
        if searchText != None:
            data = (self.queryset.filter(title__contains=searchText)
                   | self.queryset.filter(user__username__contains=searchText)
                   | self.queryset.filter(user__email__contains=searchText)
                   | self.queryset.filter(tags__name__contains=searchText)).distinct()
            return data
        return self.queryset.all()

    def get_permissions(self):
        """为文章的增删改查设置权限"""
        permission_classes = []
        print('ok: ', self.action)
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwnArticle]
        return [permission() for permission in permission_classes]



# 使用ViewSet可以直接配置路由方法，very convenient
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """权限控制方法: 使用jwt token后，restframework会自动将token解析为用户身份"""
        permission_classes = []
        # 每个人都能注册用户，查看用户
        if self.action == 'create' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        # 只有已经登陆的用户或管理员才能获取、更新、patch用户信息
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        # 只有管理员才能获取用户列表和删除用户
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer

@api_view(['GET'])
def get_user_info(request):
    """根据token获取用户信息"""
    if request.method == 'GET':
        token = request.GET.get('token')
        token_user = jwt_decode_handler(token)
        user_id = token_user['user_id']
        user_info = User.objects.get(pk=user_id)
        serializer = UserSerializer(user_info, many=False, context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
def get_user_id(request):
    """根据token获取用户id"""
    if request.method == 'GET':
        token = request.GET.get('token')
        token_user = jwt_decode_handler(token)
        return JsonResponse({'user_id': token_user['user_id']})

# class TagViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
@api_view(['GET'])
def  get_tags(request):
    """随即返回若干个标签"""
    import random
    serializers = TagSerializer(Tag.objects.all(), many=True)
    sample_size = min(5, len(serializers.data))
    return Response(random.sample(serializers.data, sample_size))

@api_view(['POST'])
def vote_up(request):
    """实现点赞功能，由于没有用到序列化器，这里先将前台传送的json二进制流解析为字典格式"""
    import json
    data = json.loads(request.body)
    id = (int)(data['id'])
    user_id = (int)(data['user_id'])
    # 如果对象不存在返回404
    if not Article.objects.filter(pk=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    article = Article.objects.get(pk=id)
    article.like_count += 1
    article.like_persons.add(User.objects.get(pk=user_id))
    article.save()
    return JsonResponse({'like_count': article.like_count})

@api_view(['POST'])
def vote_down(request):
    """取消点赞功能"""
    import json
    data = json.loads(request.body)
    id = (int)(data['id'])
    user_id = (int)(data['user_id'])
    if not Article.objects.filter(pk=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    article = Article.objects.get(pk=id)
    article.like_count -= 1
    article.like_persons.remove(User.objects.get(pk=user_id))
    article.save()
    return JsonResponse({'like_count': article.like_count})