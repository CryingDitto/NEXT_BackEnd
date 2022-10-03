from django.urls import path


from .views import PostDetail, PostList, LikeList, LikeDetail, CommentList, CommentDetail

urlpatterns = [
    # path('post/', post_list),

    path('post/', PostList.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('post/<int:post_pk>/comment/', CommentList.as_view()),
    path('post/<int:post_pk>/comment/<int:comment_pk>/', CommentDetail.as_view()),
    path('post/<int:post_pk>/like/', LikeList.as_view()),
    path('post/<int:post_pk>/like/<int:user_pk>/', LikeDetail.as_view()),
    
]

