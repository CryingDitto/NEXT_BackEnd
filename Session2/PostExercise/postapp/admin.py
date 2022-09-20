from django.contrib import admin
from .models import Major, UserInfo, Category, Comment, Post, Like

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment) 
admin.site.register(Like) 
admin.site.register(Major) 
admin.site.register(UserInfo)