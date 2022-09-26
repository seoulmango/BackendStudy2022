from rest_framework import serializers
from .models import Post, Account, Comment, User, Like

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ['title', 'content', 'category', 'author']
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'