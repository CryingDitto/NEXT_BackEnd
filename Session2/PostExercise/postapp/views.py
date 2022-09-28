#APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from rest_framework.parsers import JSONParser

#데이터
# from django.shortcuts import render, redirect
from .models import Post, Comment, Category, Major, UserInfo, Like
from .serializers import MajorSerializer, PostSerializer, UserSerializer, LikeSerializer

# Create your views here.

# function based API views - Parwiz youtube
# @csrf_exempt
# def post_list(request):
#     # get detail or read something

#     if request.method == 'GET':
#         posts = Post.objects.all()
        
#         serializer = PostSerializer(posts, many=True) #여러 객체를 serialize하기 위해 many=True로 설정
#         return JsonResponse(serializer.data, safe = False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data = data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 201) # create status
#         return JsonResponse(serializer.errors, stats = 400)

# Class based API views
# Django REST framework document
# https://www.django-rest-framework.org/tutorial/3-class-based-views/

# This blog really helped me. Super thanks!
# https://wisdom-990629.tistory.com/entry/DRF-APIView%EB%A1%9C-CRUD-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0?category=982234
class PostList(APIView):
    # post list
    def get(self, request):
        posts = Post.objects.all()
        # 여러 객체 Serialize 하기 위해 many = True로 설정
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)

    # new post
    def post(self, request):
        # request: input data
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save() # save
            return Response(serializer.data, status = status.HTTP_201_CREATED) 
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
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
        post = self.get_object(pk)
        serializer = PostSerializer(post, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    # delete post object
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


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
        return Response(status.HTTP_204_NO_CONTENT)

    def post(self, request, post_pk, user_pk):
        post = Post.objects.get(pk = post_pk)
        if post.like_users.filter(pk=user_pk).exists():
            # already like exsits
            self.delete(request, post_pk, user_pk)

        serializer = LikeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, user_pk):
        post = Post.objects.get(pk=post_pk)
        like = Like.objects.get(pk=user_pk)

        if post.like_users.filter(pk=user_pk).exists():
            like.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

        
# User Info
class UserList(APIView):
    def get(self, request):
        users = UserInfo.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_user(self, user_pk):
        try:
            return UserInfo.objects.get(pk=user_pk)
        except UserInfo.DoesNotExist:
            raise Http404
    # get detail
    def get(self, request, user_pk):
        user = self.get_user(user_pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    # edit
    def put(self, request, user_pk):
        user = self.get_user(user_pk)
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    # delete
    def delete(self, request, user_pk):
        user = self.get_user(user_pk)
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

# Major
class MajorList(APIView):
    def get(self, request):
        majors = Major.objects.all()
        # 여러 객체 Serialize 하기 위해 many = True로 설정
        serializer = MajorSerializer(majors, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MajorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class MajorDetail(APIView):
    def get_mj(self, major_pk):
        try :
            return Major.objects.get(pk=major_pk)
        except Major.DoesNotExist: 
            raise Http404
    
    def get(self, request, major_pk):
        major = Major.objects.get(pk=major_pk)
        serializer = MajorSerializer(major)
        return Response(serializer.data)

    # edit
    def put(self, request, major_pk, format=None):
        major = self.get_mj(major_pk)
        serializer = MajorSerializer(major, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)

    # delete
    def delete(self, request, major_pk, format=None):
        major = self.get_mj(major_pk)
        major.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



# Authentication (Log in, out)