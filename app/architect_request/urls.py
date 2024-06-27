"""
Module: app.urls

Description:
This module defines URL patterns for the Archimatch application using Django's path() function.
It includes routing configurations for various API endpoints using Django Rest Framework's DefaultRouter.

"""

from django.urls import include, path

from rest_framework import routers

from app.architect_request.controllers.ArchitectRequestViewSet import (
    ArchitectRequestViewSet,
)

router = routers.DefaultRouter()
router.register(
    "architect-request", ArchitectRequestViewSet, basename="architect-request"
)
urlpatterns = [
    path("", include(router.urls)),
]
