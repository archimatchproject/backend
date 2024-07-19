"""
Exposed URLs for the cms app.

This module defines the URL patterns for the BlogThematicViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.cms.controllers.BlogThematicViewSet import BlogThematicViewSet


blog_thematic_urlpatterns = [
    path(
        "blog-thematic",
        BlogThematicViewSet.as_view({"get": "list"}),
        name="blog-thematic-list",
    ),
    path(
        "blog-thematic/create/",
        BlogThematicViewSet.as_view({"post": "create"}),
        name="blog-thematic-create",
    ),
    path(
        "blog-thematic/<int:pk>/",
        BlogThematicViewSet.as_view({"get": "retrieve"}),
        name="blog-thematic-retrieve",
    ),
    path(
        "blog-thematic/update/<int:pk>/",
        BlogThematicViewSet.as_view({"put": "update"}),
        name="blog-thematic-update",
    ),
    path(
        "blog-thematic/delete/<int:pk>/",
        BlogThematicViewSet.as_view({"delete": "destroy"}),
        name="blog-thematic-delete",
    ),
    path(
        "blog-thematic/change-visibility/<int:pk>/",
        BlogThematicViewSet.as_view({"put": "change_visibility"}),
        name="blog-thematic-change-visibility",
    ),
]
