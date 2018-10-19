from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from posts.views import UserViewSet

router = routers.DefaultRouter()
router.register('user',UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
