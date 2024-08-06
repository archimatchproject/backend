"""
Module: app.urls

Description:
This module defines URL patterns for the Archimatch application using Django's path() function.
It includes routing configurations for various API endpoints using Django Rest Framework's
DefaultRouter.

"""

from django.urls import include
from django.urls import path

from rest_framework import routers

from app.moderation.routes.ArchitectReportUrls import architect_report_urlpatterns
from app.moderation.routes.ClientReviewUrls import client_review_urlpatterns
from app.moderation.routes.ProjectReportUrls import project_report_urlpatterns
from app.moderation.routes.ReviewReportUrls import review_report_urlpatterns


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    *architect_report_urlpatterns,
    *client_review_urlpatterns,
    *project_report_urlpatterns,
    *review_report_urlpatterns,
]
