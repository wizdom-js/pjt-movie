# Generated by Django 3.2.9 on 2021-11-19 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_rename_poster_path_like_like_poster_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like_movie_title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
