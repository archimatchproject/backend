"""
Module: app.urls

Description:
This module defines URL patterns for the Archimatch application using Django's path() function.
It includes routing configurations for various API endpoints using Django Rest Framework's DefaultRouter.

"""

from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from app.users.routes.AdminUrls import admin_urlpatterns
from app.users.routes.ArchimatchUserUrls import archimatch_user_urlpatterns
from app.users.routes.ClientUrls import client_urlpatterns
from app.users.routes.SupplierUrls import supplier_urlpatterns
from app.users.controllers import (
    ArchimatchUserObtainPairView,
    PhoneTokenObtainPairView,
)

router = routers.DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    *admin_urlpatterns,
    *archimatch_user_urlpatterns,
    *client_urlpatterns,
    *supplier_urlpatterns,
    path("login-email/", ArchimatchUserObtainPairView.as_view(), name="login-email"),
    path("login-phone/", PhoneTokenObtainPairView.as_view(), name="login-phone"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
