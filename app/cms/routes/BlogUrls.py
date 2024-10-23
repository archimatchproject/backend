"""
Exposed URLs for the cms app.

This module defines the URL patterns for the BlogViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.cms.controllers.BlogViewSet import BlogViewSet


blog_urlpatterns = [
    path(
        "blog",
        BlogViewSet.as_view({"get": "list"}),
        name="blog-list",
    ),
    path(
        "blog/create/",
        BlogViewSet.as_view({"post": "create"}),
        name="blog-create",
    ),
    path(
        "blog/<int:pk>/",
        BlogViewSet.as_view({"get": "retrieve"}),
        name="blog-retrieve",
    ),
    path(
        "blog/update/<int:pk>/",
        BlogViewSet.as_view({"put": "update"}),
        name="blog-update",
    ),
    path(
        "blog/delete/<int:pk>/",
        BlogViewSet.as_view({"delete": "destroy"}),
        name="blog-delete",
    ),
    path(
        "blog/update-cover-photo/<int:pk>/",
        BlogViewSet.as_view({"put": "update_cover_photo"}),
        name="blog-update-cover-photo",
    ),
    path(
        "blog/change-visibility/<int:pk>/",
        BlogViewSet.as_view({"put": "change_visibility"}),
        name="blog-change-visibility",
    ),
    path(
        "blog/upload-media/",
        BlogViewSet.as_view({"post": "upload_media"}),
        name="blog-upload-media",
    ),
    path("blog/tags", BlogViewSet.as_view({"get": "list_tags"}), name="blog-tags-list"),
]
