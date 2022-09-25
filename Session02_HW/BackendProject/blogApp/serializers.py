from rest_framework import serializers
from .models import Post, Account, Comment, User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ['title', 'content', 'category', 'author']
        fields = '__all__'