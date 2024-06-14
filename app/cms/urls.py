from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from app.cms.controllers import BlogViewSet

router = routers.DefaultRouter()
router.register('blog',BlogViewSet,basename='blog')

urlpatterns = [
    path("", include(router.urls)),
]
