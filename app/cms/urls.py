from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.cms.controllers import BlogViewSet

router = routers.DefaultRouter()
router.register("blog", BlogViewSet, basename="blog")

urlpatterns = [
    path("", include(router.urls)),
]
