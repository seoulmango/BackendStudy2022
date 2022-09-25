from unicodedata import category
from .models import Post
from .serializers import PostSerializer
# generics
from rest_framework import generics
from rest_framework import mixins
# class based
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse


# Generic API views
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'

class CatList(APIView):
    def get_posts(self, category):
        try:
            return Post.objects.filter(category=category)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, category):
        posts = self.get_posts(category).all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = PostSerializer(data=request.data)
        
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)