from django.urls import path
from apps.users.views import LoginAPIView, LogoutAPIView, ActiveAPIView
from apps.users.api.routers import userrouters

app_name = "users"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("active/", ActiveAPIView.as_view(), name="active"),
    *userrouters,
]
