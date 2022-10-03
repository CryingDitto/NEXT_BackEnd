from dataclasses import field
from rest_framework import serializers as sz
from .models import Post, Like, Comment
from accounts.models import Profile

# class PostSerializer(sz.Serializer):
class PostSerializer(sz.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'content', 'like_counts', 'like_users'] # 일부 설정
        # fields = '__all__' # 전부 설정

        read_only_fields= ['author'] 


class CommentSerializer(sz.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__' # author, post, content
        read_only_fields= ['post', 'author'] 

class LikeSerializer(sz.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'author']

# class MajorSerializer(sz.ModelSerializer):
#     class Meta:
#         model = Major
#         fields = '__all__'

# class UserSerializer(sz.ModelSerializer):
#     class Meta:
#         model = UserInfo
#         fields = '__all__'

    # function based API views
    # author = sz.ForeignKey("UserInfo", on_delete=models.CASCADE, related_name="myPost")
    # title = sz.CharField(max_length=100)
    # category = sz.ForeignKey("Category", on_delete=models.SET_NULL, null=True, related_name='post') # if category is deleted, the category of this post will be null
    # content = sz.TextField()


    # def create(self, validated_data):
    #     return Post.objects.create(validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.author = validated_data.get('author', instance.author)
    #     instance.category = validated_data.get('category', instance.category)
    #     instance.content = validated_data.get('content', instance.content)
    #     return instance

