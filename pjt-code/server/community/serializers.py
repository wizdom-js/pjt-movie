from rest_framework import serializers
from .models import Comment, Post
from django.contrib.auth import get_user_model

# 전체 영화 조회
class PostListSerializer(serializers.ModelSerializer):
    
    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True) # 패스워드는 리턴으로 나오지 않게하기 위해, serializing에는 사용이 된다.

        class Meta:
            model = get_user_model()
            fields = ('id', 'username', 'password', 'profile_image', 'nickname')

    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'user', 'created_at')
        read_only_fields = ('user_id',)


#상세 영화 조회
class PostSerializer(serializers.ModelSerializer):
    
    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True) # 패스워드는 리턴으로 나오지 않게하기 위해, serializing에는 사용이 된다.

        class Meta:
            model = get_user_model()
            fields = ('id', 'username', 'password', 'profile_image', 'nickname')

    likes_count = serializers.IntegerField(
        source='like_users.count',
        read_only=True
    )

    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'created_at', 'updated_at', 'likes_count')
        read_only_fields = ('user_id',)


class CommentSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True) # 패스워드는 리턴으로 나오지 않게하기 위해, serializing에는 사용이 된다.

        class Meta:
            model = get_user_model()
            fields = ('id', 'username', 'password', 'profile_image', 'nickname')

    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'content', 'post_id', 'user', 'created_at', 'updated_at')
        read_only_fields = ('post_id', 'user_id')


#상세 영화 조회
class PostDetailSerializer(serializers.ModelSerializer):
    
    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True) # 패스워드는 리턴으로 나오지 않게하기 위해, serializing에는 사용이 된다.

        class Meta:
            model = get_user_model()
            fields = ('id', 'username', 'password', 'profile_image', 'nickname')
        
    user = UserSerializer(read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(
        source='like_users.count',
        read_only=True
    )


    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'created_at', 'updated_at', 'comment_set', 'likes_count')
        read_only_fields = ('user_id',)