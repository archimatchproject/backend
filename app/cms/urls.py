"""
Module: app.urls

Description:
This module defines URL patterns for the Archimatch application using Django's path() function.
It includes routing configurations for various API endpoints using Django Rest Framework's DefaultRouter.

"""
from django.urls import include, path

from rest_framework import routers
from app.cms.routes.BlogUrls import blog_urlpatterns
from app.cms.controllers import BlogViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    *blog_urlpatterns
]
