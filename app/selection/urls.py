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

from app.selection.routes.SelectionUrls import selection_urlpatterns
from app.selection.routes.QuoteUrls import quote_urlpatterns

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    *selection_urlpatterns,
    *quote_urlpatterns
]
