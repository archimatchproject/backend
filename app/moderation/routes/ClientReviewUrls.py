"""
Exposed URLs for the ClientReview app.

This module defines the URL patterns for the ClientReviewViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.moderation.controllers.ClientReviewViewSet import ClientReviewViewSet


client_review_urlpatterns = [
    path(
        "client-review",
        ClientReviewViewSet.as_view({"get": "list"}),
        name="client-review-list",
    ),
    path(
        "client-review/architect-reviews",
        ClientReviewViewSet.as_view({"get": "architect_reviews"}),
        name="client-review-architect-reviews",
    ),
    path(
        "client-review/create/",
        ClientReviewViewSet.as_view({"post": "create"}),
        name="client-review-create",
    ),
    path(
        "client-review/<int:pk>",
        ClientReviewViewSet.as_view({"get": "retrieve"}),
        name="client-review-retrieve",
    ),
    path(
        "client-review/update/<int:pk>/",
        ClientReviewViewSet.as_view({"put": "update"}),
        name="client-review-update",
    ),
    path(
        "client-review/delete/<int:pk>/",
        ClientReviewViewSet.as_view({"delete": "destroy"}),
        name="client-review-delete",
    ),
]
