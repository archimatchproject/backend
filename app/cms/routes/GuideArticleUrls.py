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
]
