from django.urls import path
from .views import (CreateUser, CreateToken, VerifyUser, BlacklistRefresh,)
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (MajorList, MajorDetail, UserList, UserDetail,)

urlpatterns = [

    path('', CreateUser.as_view()),
    path('token/', CreateToken.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name = "token_refresh"),
    path('verify/', VerifyUser.as_view()),
    path('token/black/', BlacklistRefresh.as_view()),

    path('profile/', UserList.as_view()),
    path('profile/<int:user_pk>/', UserDetail.as_view()),
    path('major/', MajorList.as_view()),
    path('major/<int:major_pk>/', MajorDetail.as_view()),
]