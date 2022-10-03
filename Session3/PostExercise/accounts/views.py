from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate

#APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken # to refresh token
from rest_framework.permissions import IsAuthenticated
import json

# models
from django.contrib.auth.models import User
from .models import Major, Profile
from .serializers import MajorSerializer, ProfileSerializer

# Create your views here.
class CreateUser(APIView):
    # created an user / signup
    # do not need authentication
    permission_classes = []
    
    # create an user
    def post(self, request):
        ### using json
        # json data needs: username, password, name, student_id
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        created_user = User.objects.create_user(
            username = username,
            password = password
        )

        # create Profile model together
        profile = Profile.objects.create(
            user = created_user,
            name = data['name'],
            student_id = data['student_id'],

            # 그냥 일단 아무거나 가져왔음;;
            major_main = Major.objects.get(pk=1),
            major_sub=Major.objects.get(pk=1) 
        )


        context = {
            "msg": "user is created",
            "username": created_user.username
        }
        return Response(context, status.HTTP_201_CREATED)

    def delete(self, request):
        permission_classes = (IsAuthenticated)

        data = request.data
        username = data['username']
        password = data['password']

        if username==request.user.username & password == request.user.password:
            Profile.objects.filter(user=request.user).delete()
            User.objects.filter(username=request.user.username).delete()

# 에러나길래 유저 생성 제대로 된 거 맞는지 확인용으로 사용했음
# 이 방법 말고 방법이 있는지?
    # def get(self, request):
    #     created_user = User.objects.all()

    #     context = {
    #         "username": created_user[1].username,
    #         "password": created_user[1].password
    #     }


        # return Response(context)

# 일종의 로그인
# username, password가 일치해야만 토큰 발급하므로
class CreateToken(APIView):
    # create the first token
    # the user can be authenticated or authorized after creating token
    permission_classes = []

    # create token
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        # if the user does not exist
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZATION)
        
        # the user exists
        refresh = RefreshToken.for_user(user)
        context = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        res = Response(context, status=status.HTTP_201_CREATED)
        # res.set_cookie('access_token', refresh.access_token)
        return res


class VerifyUser(APIView):
    permission_classes = (IsAuthenticated,)
    
    # check if the user is super user or not
    # read user info
    def get(self, request):
        if request.user.is_superuser:
            context = {
                'msg': 'The user is superuser.'
            }
            return Response(context, status=status.HTTP_200_OK)
        
        context={
            'msg': 'The user is ordinary user.'
        }
        return Response(context, status=status.HTTP_200_OK)
    
# Log out!!
# https://medium.com/grad4-engineering/how-to-blacklist-json-web-tokens-in-django-43fb88ae3d17
# https://stackoverflow.com/questions/58010776/how-to-blacklist-a-jwt-token-with-simple-jwt-django-rest
class BlacklistRefresh(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = json.loads(request.body)
        refreshToken = RefreshToken(data['refresh'])
        refreshToken.blacklist()
        ### Blacklist the refresh token: extract token from the header
        ### during logout request user and refresh token is provided"""
        # 근데 그냥 쿠키에 남아있는 access token 지우면 될 것 같기도...

        context = {
            'msg': 'Log out.'
        }
        return Response(context, status=status.HTTP_200_OK)
        
        
        # response = Response(context, status = status.HTTP_202_ACCEPTED)
        # response.delete_cookie('refresh')



# User Info
class UserList(APIView):
    def get(self, request):
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many = True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = ProfileSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status = status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    # permission_classes = (IsAuthenticated,)

    def get_user(self, user_pk):
        user = get_object_or_404(Profile, pk = user_pk)
        return user
        # try:
        #     return Profile.objects.get(pk=user_pk)
        # except Profile.DoesNotExist:
        #     raise Http404

    # get detail
    def get(self, request, user_pk):
        user = self.get_user(user_pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    # edit
    def put(self, request, user_pk):
        # user = self.get_user(user_pk)
        user = request.user
        serializer = ProfileSerializer(user, data = request.data)
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
        major = get_object_or_404(Major, pk=major_pk)
        return major
        # try :
        #     return Major.objects.get(pk=major_pk)
        # except Major.DoesNotExist: 
        #     raise Http404
    
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



