from django.urls import path
from .views import PostList, PostDetail, CatList

urlpatterns = [
    # All posts list
    path('postlist/', PostList.as_view()),
    # Categorized list
    path('postlist/<int:category>/', CatList.as_view()),
    # Detail page
    path('post/<int:id>/', PostDetail.as_view()),
]