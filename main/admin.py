from django.contrib import admin
from .models import Product, Article, Tag, Profile, Vote

# Register your models here.
admin.site.register(Product)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Vote)