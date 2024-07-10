"""
exposed URLS for architect_realization app
viewset : Realization viewset
"""

from django.urls import path

from app.architect_realization.controllers.RealizationViewSet import RealizationViewSet


architect_realization_urlpatterns = [
    path(
        "create-realization/",
        RealizationViewSet.as_view({"post": "realization_create"}),
        name="create-realization",
    ),
    path(
        "all-realizations/",
        RealizationViewSet.as_view({"get": "get"}),
        name="get-all-realizations",
    ),
    path(
        "architectural-styles/",
        RealizationViewSet.as_view({"get": "get_architectural_styles"}),
        name="architectural-styles",
    ),
    path(
        "needs/",
        RealizationViewSet.as_view({"get": "get_needs"}),
        name="needs",
    ),
]
