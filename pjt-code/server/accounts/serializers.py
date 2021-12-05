from rest_framework import serializers
from django.contrib.auth import get_user_model
from community.models import Comment, Post
from movie.models import Like, Review

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # 패스워드는 리턴으로 나오지 않게하기 위해, serializing에는 사용이 된다.

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'profile_image', 'nickname', 'email',)


class FollowSerializer(serializers.ModelSerializer):

    class CommentSerializer(serializers.ModelSerializer):

        class Meta:
            model = Comment
            fields = ('id', 'content', 'post_id', 'created_at')
            read_only_fields = ('post_id', 'user_id')

    class PostSerializer(serializers.ModelSerializer):

        class Meta:
            model = Post
            fields = ('id', 'title', 'created_at')
            read_only_fields = ('user_id',)

    comment_set = CommentSerializer(many=True, read_only=True)
    post_set = PostSerializer(many=True, read_only=True)
    #팔로워 유저들 정보, 팔로잉 유저들 정보
    followers = UserSerializer(many=True, read_only=True)
    followings = UserSerializer(many=True, read_only=True)

    # 팔로잉수, 팔로워수, 팔로우 여부
    followers_count = serializers.IntegerField(
        source='followers.count',
        read_only=True
    )
    followings_count = serializers.IntegerField(
        source='followings.count',
        read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'profile_image', 'followers', 'followings', 'followers_count', 'followings_count',  'comment_set', 'post_set')


class ProfileSerializer(serializers.ModelSerializer):

    class CommentSerializer(serializers.ModelSerializer):

        class Meta:
            model = Comment
            fields = ('id', 'content', 'post_id', 'created_at')
            read_only_fields = ('post_id', 'user_id')

    class PostSerializer(serializers.ModelSerializer):

        class Meta:
            model = Post
            fields = ('id', 'title', 'created_at')
            read_only_fields = ('user_id',)

    class MovieLikeSerializer(serializers.ModelSerializer):

        class Meta:
            model = Like
            fields = ('movie_id', 'like_movie_title', 'like_poster_path')
    
    class MovieReviewSerializer(serializers.ModelSerializer):

        class Meta:
            model = Review
            fields = ('id', 'movie_id', 'movie_title', 'poster_path', 'created_at', 'content', 'rank')
    

    comment_set = CommentSerializer(many=True, read_only=True)
    post_set = PostSerializer(many=True, read_only=True)
    #팔로워 유저들 정보, 팔로잉 유저들 정보
    followers = UserSerializer(many=True, read_only=True)
    followings = UserSerializer(many=True, read_only=True)

    # 팔로잉수, 팔로워수, 팔로우 여부
    followers_count = serializers.IntegerField(
        source='followers.count',
        read_only=True
    )
    followings_count = serializers.IntegerField(
        source='followings.count',
        read_only=True
    )
    post_count = serializers.IntegerField(
        source='post_set.count',
        read_only=True
    )
    comment_count = serializers.IntegerField(
        source='comment_set.count',
        read_only=True
    )
    like_post_count = serializers.IntegerField(
        source='like_posts.count',
        read_only=True
    )
    review_count = serializers.IntegerField(
        source='review_set.count',
        read_only=True
    )

    like_posts = PostSerializer(many=True, read_only=True)
    like_movie = MovieLikeSerializer(many=True, read_only=True)
    review_set = MovieReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'profile_image', 'email', 'followers', 'followings', 'followers_count', 'followings_count',  'comment_set', 'post_set', 'comment_count', 'post_count', 'like_posts', 'like_post_count', 'like_movie', 'review_set', 'review_count', 'is_superuser')


class FollowerSerializer(serializers.ModelSerializer):
    followers = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('followers',)


class ProfileChangeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'profile_image', 'email')
        read_only_fields = ('username', 'password')

class PasswordChangeSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True) # 패스워드는 리턴으로 나오지 않게하기 위해, serializing에는 사용이 된다.

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'password', 'profile_image', 'email')
        read_only_fields = ('username', 'nickname')
