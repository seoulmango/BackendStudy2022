from .models import Post, Category, User, Like, Comment, Account
from .serializers import CommentSerializer, LikeSerializer, PostSerializer, AccountSerializer
# class based
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse

# 전체 포스트 리스트 (새로운 포스트 작성도 여기서 이뤄진다.)
class PostList(APIView):
    # access to all data from db
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 포스트 디테일. 댓글이 있다면 댓글도 함께 보인다.
class PostDetail(APIView):
    def get_post(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    # 댓글이 있다면 가져온다.
    def get_comments(self, id):
        try:
            return Comment.objects.filter(post=self.get_post(id))
        except Comment.DoesNotExist:
            return 0

    # 좋아요가 있다면 가져온다.
    def get_likes(self, id):
        try:
            return Like.objects.get(post=self.get_post(id))
        except Like.DoesNotExist:
            return 0

    def get(self, request, id):
        post = self.get_post(id)
        comments = self.get_comments(id)

        # 좋아요도 함께 보여줄려면 if문이 너무 많아진다...
        # like = self.get_likes(id)
        # lserializer = LikeSerializer(like)

        pserializer = PostSerializer(post)
        # 댓글이 있는 포스트는 댓글까지 함께 보여준다.
        if comments:
            cserializer = CommentSerializer(comments, many=True)
            return Response((pserializer.data, cserializer.data), status=status.HTTP_200_OK)
        return Response(pserializer.data)

    def put(self, request, id):
        post = self.get_post(id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = self.get_post(id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 전체 리스트에서 특정 카테고리만 선택
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

# 댓글 생성
class NewComment(APIView):
    def get_post(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        post = self.get_post(id)
        pserializer = PostSerializer(post)
        return Response(pserializer.data)
    
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 수정/삭제
class CommentDetail(APIView):
    def get_comment(self, id):
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        comment = self.get_comment(id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, id):
        comment = self.get_comment(id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        comment = self.get_comment(id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleLike(APIView):
    # 좋아요 그룹이 있다면 그 그룹을 리턴, 없으면 생성 후 리턴 (이 때 로그인 돼 있는 사람을 좋아요에 추가함)
    def get_like(self, postid):
        try:
            return Like.objects.get(post=Post.objects.get(id=postid))
        except Like.DoesNotExist:
            newlike = Like(post=Post.objects.get(id=postid))
            newlike.save()
            return Like.objects.get(post=Post.objects.get(id=postid))

    # 좋아요 리스트 조회
    def get(self, request, postid):
        like = self.get_like(postid)
        serializer = LikeSerializer(like)
        return Response(serializer.data)
    
    # 좋아요 / 좋아요 취소
    def post(self, request, postid):
        like = self.get_like(postid)
        account = Account.objects.get(user=request.user)

        # 좋아요를 누른 사람이었다면? 좋아요 취소
        if account in like.like_users.all():
            like.like_users.remove(account)
            like.save()
        # 좋아요를 처음 눌렀다면? 좋아요 추가
        else:
            like.like_users.add(account)
            like.save()

        serializer = LikeSerializer(like)
        return Response(serializer.data)
        
        
    
# 계정 RUD 기능
class AccountEdit(APIView):
    def get_account(self, userid):
        try:
            return Account.objects.get(userid=userid)
        except Account.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, userid):
        account = self.get_account(userid)
        serializer = AccountSerializer(account)      
        return Response(serializer.data)

    def put(self, request, userid):
        account = self.get_account(userid)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, userid):
        account = self.get_account(userid)
        user = request.user
        account.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 계정 생성
class SignUp(APIView):
    # ((임시)) 모든 계정 다 보여주기.
    # 나중에 회원가입 창만 보여주는 것으로 바꿀 것!
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

