from django.contrib import admin
from .models import Category, Post, Comment, Account, Like, School, Administration
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Account)
admin.site.register(Like)
admin.site.register(School)
admin.site.register(Administration)