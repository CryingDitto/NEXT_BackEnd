#APIView
from rest_framework.views import APIView
from rest_framework.response import Response #response
from rest_framework import status

from rest_framework.parsers import JSONParser

# for authorization 
# from rest_framework.decorators import permission_classes # decorator 방식
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# response code
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import get_object_or_404
# models, data
# from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Post, Comment, Category, Like
from accounts.models import Profile
from .serializers import CommentSerializer, PostSerializer, PostEditSerializer, LikeSerializer


# Class based API views
# Django REST framework document
# https://www.django-rest-framework.org/tutorial/3-class-based-views/

# This blog really helped me. Super thanks!
# https://wisdom-990629.tistory.com/entry/DRF-APIView%EB%A1%9C-CRUD-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0?category=982234
class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # post list
    def get(self, request):
        posts = Post.objects.all()
        # 여러 객체 Serialize 하기 위해 many = True로 설정
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)

    # @permission_classes([IsAuthenticated])
    # new post
    def post(self, request):
        permission_classes = (IsAuthenticated,)

        # request: input data
        # prepare author data & fix
        author = Profile.objects.get(user=request.user)

        # This QueryDict instance is immutble
        # Thus, to edit the author data, data's _mutable property should be changed
        # How To Fix Mutability: https://www.youtube.com/watch?v=MzgMdl-k3XI
        # 근데 처음부터 request에 author를 안 받고 그냥 request.user로 처리하는 방법 없나? ㅠㅠ

        # data = request.data
        # _mutable = data._mutable # original state
        # data._mutable = True
        # data['author'] = str(author.pk)
        # data._mutable = _mutable # return to original state

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = author) # save
            return Response(serializer.data, status = status.HTTP_201_CREATED) 
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # get Post object
    def get_object(self, pk):
        try:
            return Post.objects.get(pk = pk)
        except Post.DoesNotExist:
            raise Http404
    
    # get detail of each Post object
    def get(self, request, pk, format = None):
        post = self.get_object(pk)
        post.like_count = post.like_users.count()
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # edit detail of post    
    def put(self, request, pk, format = None):
        permission_classes = (IsAuthenticated,)
        post = self.get_object(pk)

        # post.author는 Profile이므로 post.author.user와 비교해야 함
        # 사실 그냥 User 상속하면 됨
        if(post.author.user == request.user):
            serializer = PostSerializer(post, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            context = {"msg":'Wrong request. This post is not yours.'}
            return Response(context, status = status.HTTP_403_FORBIDDEN)


    # delete post object
    def delete(self, request, pk, format=None):
        permission_classes = (IsAuthenticated,)
        post = self.get_object(pk)

        # post.author는 Profile이므로 post.author.user와 비교해야 함
        if (post.author.user == request.user):
            post.delete()
            context = {"msg": 'Your post is deleted.'}
            return Response(context, status = status.HTTP_204_NO_CONTENT)
        context = {"msg":'Wrong request. This post is not yours.'}
        return Response(context, status = status.HTTP_403_FORBIDDEN)

class CommentList(APIView):
    def get_comment(self, post_pk):
        post = get_object_or_404(Post, pk = post_pk)
        comments = Comment.objects.filter(post = post)
        return comments
    
    def get(self, request, post_pk):
        comments = self.get_comment(post_pk)

        if comments is None:
            context = {"msg": "No comments yet."}
            return Response(context, status = status.HTTP_204_NO_CONTENT)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data)

    def post(self, request, post_pk):
        permission_classes = (IsAuthenticated,)
        post = get_object_or_404(Post, pk = post_pk)
        user = request.user

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            serializer.save(post=post, author = Profile.objects.get(user = user)) # 해당 글에 댓글쓰기
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        context = {"msg":'Forbidden. You are not allowed to write comments.'}
        return Response(context, status = status.HTTP_403_FORBIDDEN)

class CommentDetail(APIView):
    permission_classes = (IsAuthenticated,)
    # get detailed comment info
    def get(self, request, post_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)

        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # edit comment
    def put(self, request, post_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        # serializer = CommentSerializer(comment)
        if(comment.author.user == request.user):
            serializer = CommentSerializer(comment, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data) # edit success
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            context = {"msg":'Wrong request. This post is not yours.'}
            return Response(context, status = status.HTTP_403_FORBIDDEN)

    # delete comment
    def delete(self, request, post_pk, comment_pk):
        comment = get_object_or_404(Comment, pk = comment_pk)
        if(comment.author.user == request.user):
            comment.delete()
            context = {"msg": 'Your comment #'+comment_pk+' is deleted.'}
            # delete success
            return Response(context, status = status.HTTP_204_NO_CONTENT)
        context = {"msg":'Wrong request. This comment is not yours.'}
        return Response(context, status = status.HTTP_403_FORBIDDEN)



    

    


    # def put_like(self, request, pk):
    #     post = self.get_object(pk)
    #     like = Like.objects.filter(post=post)[0]

    #     serializer = LikeSerializer(like, data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    
    # def get_like(self, request, pk):
    #     try:
    #         like = Like.objects.filter(post=Post.objects.get(pk))
    #         # like = Like.objects.filter(post=PostDetail.get_object(pk))
    #         return like
    #     except Like.DoesNotExist:
    #         return Http404
    
    # def get(self, request, pk):
    #     likes = self.get_like(pk)
    #     serializer = LikeSerializer(likes, many = True)
    #     return Response(serializer.data)


class LikeList(APIView):
    # get like objects of current post
    def get_like(self, post_pk):
        try:
            like = Like.objects.filter(post=Post.objects.get(pk=post_pk))
            return like
        except Like.DoesNotExist:
            return Http404

    def get(self, request, post_pk, format = None):
        # post = Post.objects.get(pk = post_pk)
        likes = self.get_like(post_pk)
        serializer = LikeSerializer(likes, many = True)
        return Response(serializer.data)

class LikeDetail(APIView):
    # get like
    def get(self, request, post_pk, user_pk):
        post = Post.objects.get(pk = post_pk)
        if post.like_users.filter(pk=user_pk).exists():
            like = Like.objects.get(pk=user_pk) # my like
            serializer = LikeSerializer(like)
            return Response(serializer.data)

        context = {"msg": "You didn't push like on this post."}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, post_pk, user_pk):
        permission_classes = (IsAuthenticated,)
        post = Post.objects.get(pk = post_pk)
        if post.like_users.filter(pk=user_pk).exists():
            # already like exsits
            self.delete(request, post_pk, user_pk)

        # 이렇게 넣어주는 방법 밖에는 없는지...? ㅠㅠ
        # author를 serializer에서 제외하면서도 request.user를 like model에 직접 넣어주는 방법은 없는지..?
        data = request.data
        data.author = request.user
        serializer = LikeSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk):
        post = Post.objects.get(pk=post_pk)
        like = Like.objects.get(author=request.user)

        if post.like_users.filter(author=request.user).exists():
            like.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

