from rest_framework import serializers
from .models import Review, Like, CrawledMovie
from django.contrib.auth import get_user_model

class LikeSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True) # 패스워드는 리턴으로 나오지 않게하기 위해, serializing에는 사용이 된다.

        class Meta:
            model = get_user_model()
            fields = ('id', 'username', 'password', 'profile_image', 'nickname')

    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ('user', 'movie_id')
        read_only_fields = ('user_id',)

class ReviewSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True) # 패스워드는 리턴으로 나오지 않게하기 위해, serializing에는 사용이 된다.

        class Meta:
            model = get_user_model()
            fields = ('id', 'username', 'password', 'profile_image', 'nickname')

    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'user', 'movie_id', 'content', 'rank', 'is_spoiler', 'created_at', 'updated_at')
        read_only_fields = ('user_id', 'movie_id')

class CrawledMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrawledMovie
        fields = ('movie_id', 'title', 'poster_path', 'backdrop_path')
       