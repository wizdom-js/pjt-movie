# Generated by Django 3.2.9 on 2021-11-20 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_like_like_movie_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='title',
        ),
    ]