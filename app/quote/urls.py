"""
Module: app.qote

Description:
This module defines URL patterns for the Archimatch application using Django's path() function.
It includes routing configurations for various API endpoints using Django Rest Framework's
DefaultRouter.

"""

from django.urls import include
from django.urls import path

from rest_framework import routers

# from app.recommendation.routes.ArchitectBoxUrls import box_urlpatterns
# from app.recommendation.routes.RecommendationSettingsUrls import recommendation_settings_urlpatterns


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    # *box_urlpatterns,
    # *recommendation_settings_urlpatterns,
]
