from django.db import models
from django.conf import settings
# Create your models here.

class Review(models.Model):
    movie_id = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    rank = models.IntegerField()
    movie_title = models.TextField()
    poster_path = models.TextField()
    is_spoiler = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Like(models.Model):
    movie_id = models.CharField(max_length=10)
    like_poster_path = models.TextField(null=True)
    like_movie_title = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_movie')

    def __str__(self):
        return self.like_movie_title

class CrawledMovie(models.Model):
    movie_id = models.CharField(max_length = 10, primary_key=True)
    title = models.CharField(max_length=100, null=True)
    original_title = models.CharField(max_length=50, null=True)
    genre_1 = models.CharField(max_length=10, null=True)
    genre_2 = models.CharField(max_length=10, null=True)
    genre_3 = models.CharField(max_length=10, null=True)
    genre_4 = models.CharField(max_length=10, null=True)
    budget = models.IntegerField(null=True)
    overview = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    country_1 = models.CharField(max_length=30, null=True)
    country_2 = models.CharField(max_length=30, null=True)
    country_3 = models.CharField(max_length=30, null=True)
    release_date = models.DateField(null=True)
    runtime = models.IntegerField(null=True)
    vote_average = models.FloatField(null=True)
    vote_count =models.IntegerField(null=True)
    poster_path = models.TextField(null=True)
    backdrop_path = models.TextField(null=True)

    def __str__(self):
        return self.title



