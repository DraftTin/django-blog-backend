from rest_framework import serializers
from .models import Comment
from blog.models import User

class UserDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ParentCommentSerializer(serializers.ModelSerializer):
    """只需要(username, content)"""
    user = UserDescSerializer(required=False, allow_null=True, read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content']
        extra_kwargs = {'created': {'read_only': True}}

class CommentSerializer(serializers.ModelSerializer):
    # 只读返回username方便前端显示
    user = UserDescSerializer(required=False, allow_null=True, read_only=True)
    quote_comment = ParentCommentSerializer(required=False, allow_null=True, read_only=True)
    # 只写用在前端向后端提交评论
    user_id = serializers.IntegerField(required=True, write_only=True)
    quote_comment_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    article_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_id', 'content', 'created', 'like_count', 'quote_comment', 'quote_comment_id', 'article_id']
        extra_kwargs = { 'created': {'read_only': True} }

