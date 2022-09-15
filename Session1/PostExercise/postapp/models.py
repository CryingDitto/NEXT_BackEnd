from django.db import models

# Create your models here.
class Major(models.Model):
    type = models.CharField(max_length=20) # 본전공 심화 이중 융합
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

class UserInfo(models.Model):
    student_id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    major_main = models.ForeignKey("Major", on_delete=models.SET_NULL, related_name="student_main", null = True)
    major_sub = models.ForeignKey("Major", on_delete=models.SET_NULL, related_name="student_sub", null = True)

class Category(models.Model):
    name = models.CharField(max_length = 100)
class Comment(models.Model):
    content = models.TextField()
class Post(models.Model):
    author = models.ForeignKey("UserInfo", on_delete=models.CASCADE, related_name="myPost")
    title = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, related_name='post') # if category is deleted, the category of this post will be null
    content = models.TextField()
    
    like_count = models.PositiveIntegerField(default=0, help_text="The number of likes in the current post")


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete = models.CASCADE, related_name = "likes")
    author = models.ForeignKey("UserInfo", on_delete=models.CASCADE, related_name="myLike")

    