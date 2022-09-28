from django.urls import path
from .views import PostDetail, PostList, MajorList, MajorDetail, UserList, UserDetail, LikeList, LikeDetail

urlpatterns = [
    # path('post/', post_list),

    path('post/', PostList.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('post/<int:post_pk>/like/', LikeList.as_view()),
    path('post/<int:post_pk>/like/<int:user_pk>/', LikeDetail.as_view()),
    path('user/', UserList.as_view()),
    path('user/<int:user_pk>/', UserDetail.as_view()),

    
    path('major/', MajorList.as_view()),
    path('major/<int:major_pk>/', MajorDetail.as_view()),
]