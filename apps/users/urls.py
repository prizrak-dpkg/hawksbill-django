from django.urls import path
from apps.users.views import (
    LoginAPIView,
    LogoutAPIView,
    ActiveAPIView,
    UserData,
    UserToken,
    TokenExpired,
)
from apps.users.api.routers import userrouters

app_name = "users"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("active/", ActiveAPIView.as_view(), name="active"),
    path("gettoken/", UserToken.as_view(), name="gettoken"),
    path("userdata/", UserData.as_view(), name="userdata"),
    path("token/", TokenExpired.as_view(), name="token"),
    *userrouters,
]
