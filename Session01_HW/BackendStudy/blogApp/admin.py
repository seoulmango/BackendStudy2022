from django.contrib import admin
from .models import Post, Account, Comment
# Register your models here.

admin.site.register(Post)
admin.site.register(Account)
admin.site.register(Comment)