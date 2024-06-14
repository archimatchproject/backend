from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = routers.DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
]
