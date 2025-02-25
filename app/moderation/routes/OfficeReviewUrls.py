"""
Exposed URLs for the OfficeReview app.

This module defines the URL patterns for the OfficeReviewViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.moderation.controllers.OfficeReviewViewSet import OfficeReviewViewSet


office_review_urlpatterns = [
    path(
        "office-review",
        OfficeReviewViewSet.as_view({"get": "list"}),
        name="office-review-list",
    ),
    path(
        "office-review/architect-reviews/<int:pk>/",
        OfficeReviewViewSet.as_view({"get": "architect_reviews"}),
        name="office-review-architect-reviews",
    ),
    path(
        "office-review/architect-stats/<int:pk>/",
        OfficeReviewViewSet.as_view({"get": "architect_stats"}),
        name="office-review-architect-stats",
    ),
    path(
        "office-review/create/",
        OfficeReviewViewSet.as_view({"post": "create"}),
        name="office-review-create",
    ),
    path(
        "office-review/<int:pk>",
        OfficeReviewViewSet.as_view({"get": "retrieve"}),
        name="office-review-retrieve",
    ),
    path(
        "office-review/<int:pk>/update/",
        OfficeReviewViewSet.as_view({"put": "update"}),
        name="office-review-update",
    ),
    path(
        "office-review/delete/<int:pk>/",
        OfficeReviewViewSet.as_view({"delete": "destroy"}),
        name="office-review-delete",
    ),
]
