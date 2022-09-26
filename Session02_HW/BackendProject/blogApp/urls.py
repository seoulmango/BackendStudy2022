from django.urls import path
from .views import PostList, PostDetail, CatList, CommentDetail, AccountEdit, SignUp, ToggleLike, NewComment

urlpatterns = [
    # All posts list
    path('postlist/', PostList.as_view()),
    # Categorized list
    path('postlist/<int:category>/', CatList.as_view()),
    # Post detail page
    path('post/<int:id>/', PostDetail.as_view()),
    # New Comment
    path('post/<int:id>/newcomment', NewComment.as_view()),
    # Comment detail page
    path('comment/<int:id>/', CommentDetail.as_view()),
    # Account edit page
    path('account/<str:userid>/', AccountEdit.as_view()),
    # Signup page
    path('signup/', SignUp.as_view()),
    # Like page
    path('like/<int:postid>/', ToggleLike.as_view()),
]