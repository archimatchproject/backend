"""
Exposed URLs for the cms app.

This module defines the URL patterns for the GuideArticleViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.cms.controllers.GuideArticleViewSet import GuideArticleViewSet


guide_article_urlpatterns = [
    path(
        "guide-article",
        GuideArticleViewSet.as_view({"get": "list"}),
        name="guide-article-list",
    ),
    path(
        "guide-article/create/",
        GuideArticleViewSet.as_view({"post": "create"}),
        name="guide-article-create",
    ),
    path(
        "guide-article/<int:pk>",
        GuideArticleViewSet.as_view({"get": "retrieve"}),
        name="guide-article-detail",
    ),
    path(
        "guide-article/update/<int:pk>/",
        GuideArticleViewSet.as_view({"put": "update"}),
        name="guide-article-update",
    ),
    path(
        "guide-article/delete/<int:pk>/",
        GuideArticleViewSet.as_view({"delete": "destroy"}),
        name="guide-article-delete",
    ),
    path(
        "guide-article/change-visibility/<int:pk>/",
        GuideArticleViewSet.as_view({"put": "change_visibility"}),
        name="guide-article-change-visibility",
    ),
    path(
        "guide-article/upload-media/",
        GuideArticleViewSet.as_view({"post": "upload_media"}),
        name="guide-article-upload-media",
    ),
]
