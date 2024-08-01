"""
Exposed URLs for the cms app.

This module defines the URL patterns for the GuideThematicViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.cms.controllers.GuideThematicViewSet import GuideThematicViewSet


guide_thematic_urlpatterns = [
    path(
        "guide-thematic",
        GuideThematicViewSet.as_view({"get": "list"}),
        name="guide-thematic-list",
    ),
    path(
        "guide-thematic/create/",
        GuideThematicViewSet.as_view({"post": "create"}),
        name="guide-thematic-create",
    ),
    path(
        "guide-thematic/<int:pk>",
        GuideThematicViewSet.as_view({"get": "retrieve"}),
        name="guide-thematic-detail",
    ),
    path(
        "guide-thematic/update/<int:pk>/",
        GuideThematicViewSet.as_view({"put": "update"}),
        name="guide-thematic-update",
    ),
    path(
        "guide-thematic/delete/<int:pk>/",
        GuideThematicViewSet.as_view({"delete": "destroy"}),
        name="guide-thematic-delete",
    ),
    path(
        "guide-thematic/change-visibility/<int:pk>/",
        GuideThematicViewSet.as_view({"put": "change_visibility"}),
        name="guide-thematic-change-visibility",
    ),
]
