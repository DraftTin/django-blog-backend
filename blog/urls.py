from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

# DefaultRouter为资源定义了标准的REST方式
router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')
router.register('user', UserViewSet, basename='user')
# router.register('tag', TagViewSet, basename='tag')
# router.register('userprofile', UserProfileViewSet, basename='userprofile')
# router.register('viewset', viewset, basename='viewset')
# # path('viewset', include(router.urls), name='viewset')
urlpatterns = [
    path('', include(router.urls)),
    path('userinfo/', get_user_info, name='get_user_info'),
    path('userid/', get_user_id, name='get_user_id'),           # 通过
    path('tag/', get_tags, name='get_tags'),                    # 接受GET请求，获取标签的列表，权限: 无
    path('voteup/', vote_up, name='vote_up'),
    path('votedown/', vote_down, name='vote_down'),
]
