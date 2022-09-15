from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 대학의 모든 전공들
class School(models.Model):
    name = models.TextField()

# 본전공 + 이중/복수/융합 전공
class Administration(models.Model):
    major = models.ForeignKey(School, on_delete=models.CASCADE, related_name="administration")
    minor = models.ForeignKey(School, on_delete=models.CASCADE, related_name="administration")

# 계정 정보
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account")
    userid = models.TextField()
    userpw = models.TextField()
    username = models.TextField()
    administration = models.ForeignKey(Administration,  on_delete=models.CASCADE, related_name="account")

# 포스트 카테고리
class Category(models.Model):
    name = models.TextField()
    code = models.TextField()

# 포스트 정보
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ManyToManyField(Category, on_delete=models.CASCADE, related_name="posts")
    title = models.TextField()
    content = models.TextField()

# 댓글 정보
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    # 해당 포스트
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    # 좋아요를 누른 계정들
    like_users = models.ManyToManyField(Account, related_name="mylikes")