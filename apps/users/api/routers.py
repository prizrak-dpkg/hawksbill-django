from typing import List
from django.urls import URLPattern
from rest_framework.routers import DefaultRouter
from apps.users.api.viewsets import UserViewSet


router = DefaultRouter()
router.register(prefix=r"users", viewset=UserViewSet, basename="users")

userrouters: List[URLPattern] = router.urls
