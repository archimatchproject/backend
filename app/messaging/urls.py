"""
Module: app.urls

Description:
This module defines URL patterns for the Archimatch application using Django's path() function.
It includes routing configurations for various API endpoints using Django Rest Framework's
DefaultRouter.

"""

from django.urls import include
from django.urls import path

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from app.messaging.routes.MessageUrls import message_urlpatterns


router = DefaultRouter()
router.register("devices", FCMDeviceAuthorizedViewSet)


urlpatterns = [path("", include(router.urls)), *message_urlpatterns]
