from django.contrib import admin

# Register your models here.
from .models import Review, Like, CrawledMovie
# Register your models here.
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(CrawledMovie)