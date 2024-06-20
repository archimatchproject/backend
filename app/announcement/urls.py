"""
Module: app.urls

Description:
This module defines URL patterns for the Archimatch application using Django's path() function.
It includes routing configurations for various API endpoints using Django Rest Framework's DefaultRouter.

"""
from django.urls import include, path

from rest_framework import routers

from app.announcement.controllers import AnnouncementViewSet

router = routers.DefaultRouter()
router.register("announcement", AnnouncementViewSet, basename="announcement")

urlpatterns = [
    path("", include(router.urls)),
]
