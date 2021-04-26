from rest_framework import serializers
from .models import *
from comment.serializers import CommentSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        # 将name字段的unique检查移除
        extra_kwargs = {
            'name': {'validators': [] }
        }

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'value']

class UserProfileSerializer(serializers.ModelSerializer):
    """序列化用户的个人信息"""
    photo = AvatarSerializer(read_only=True)    # 设置read_only表示写回数据库时不需要提供该字段的信息
    # photo_id被自动映射到Avatar表
    photo_id = serializers.IntegerField(write_only=True,    # 设置write_only表示该字段只需要在写回的时候需要提供
                                        allow_null=True,
                                        required=False)
    class Meta:
        fields = ('intro', 'country', 'city', 'zip', 'address', 'photo_id', 'photo')
        model = UserProfile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """profile表示该用户的UserProfile外键, 使用UserProfileSerializer进行序列化"""
    profile = UserProfileSerializer(required=False)     # required=False表示序列化字段中可以没有profile
    class Meta:
        model = User
        fields = ('url', 'id', 'email', 'username', 'password', 'profile')
        # 只写意味着该属性只用于反序列化而不用于序列化
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile = None
        if 'profile' in validated_data:
            profile = validated_data.pop('profile') # pop操作能够使序列化数据中排除和user本身无关的部分
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # 如果序列化数据中包含profile信息，则自动填入
        if profile != None:
            userProfile = UserProfile(**profile)         # 单独创建外键对象, **profile
        else:
            userProfile = UserProfile()
        print(userProfile.photo.value)
        userProfile.user = user
        userProfile.save()
        return user

    def update(self, instance, validated_data):
        """重写父类更新方法"""
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = instance.profile
            profile.address = profile_data.get('address', profile.address)
            profile.country = profile_data.get('country', profile.country)
            profile.city = profile_data.get('city', profile.city)
            profile.zip = profile_data.get('zip', profile.zip)
            profile.photo_id = profile_data.get('photo_id', profile.photo_id)       # 修改外键
            profile.intro = profile_data.get('intro', profile.intro)
            profile.save()
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        # instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        return instance

class ArticleDetailSerializer(serializers.ModelSerializer):
    # tags = serializers.SlugRelatedField(
    #     queryset=Tag.objects.all(),
    #     many=True,
    #     required=False,
    #     slug_field='name'
    # )
    tags = TagSerializer(required=False, many=True)     # 嵌套序列化，方便直接使用序列化的数据处理外键
    comments = CommentSerializer(required=False, many=True, read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        required=False,
        many=False,
        slug_field='username',
    )
    user_id = serializers.IntegerField(read_only=True)
    html_body = serializers.SerializerMethodField()
    html_topic = serializers.SerializerMethodField()
    def get_html_body(self, obj):
        """obj为已经序列化对象的实例"""
        return obj.getMd()[0]

    def get_html_topic(self, obj):
        """obj为已经序列化对象的实例"""
        return obj.getMd()[1]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        article = Article(**validated_data)
        article.save()
        for tag in tags:
            tagName = tag['name']
            # 创建新的标签，如果标签不存在则创建并添加外键
            if not Tag.objects.filter(name=tagName).exists():
                newTag = Tag(name=tagName)
                newTag.save()
                newTag.articles.add(article)
                newTag.save()
            # 如果标签存在，则只添加外键
            else:
                tag = Tag.objects.get(name=tagName)
                tag.articles.add(article)
                tag.save()
        return article

    def update(self, instance, validated_data):
        print(validated_data)
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.tags.clear()
        instance.save()
        tags = validated_data.pop('tags')
        for tag in tags:
            tagName = tag['name']
            # 创建新的标签，如果标签不存在则创建并添加外键
            if not Tag.objects.filter(name=tagName).exists():
                newTag = Tag(name=tagName)
                newTag.save()
                newTag.articles.add(instance)
                newTag.save()
            # 如果标签存在，则只添加外键
            else:
                tag = Tag.objects.get(name=tagName)
                tag.articles.add(instance)
                tag.save()
        return instance

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'like_persons': {'read_only': True }
        }
