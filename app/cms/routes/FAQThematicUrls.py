"""
Exposed URLs for the cms app.

This module defines the URL patterns for the FAQThematicViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.cms.controllers.FAQThematicViewSet import FAQThematicViewSet


faq_thematic_urlpatterns = [
    path(
        "faq-thematic",
        FAQThematicViewSet.as_view({"get": "list"}),
        name="faq-thematic-list",
    ),
    path(
        "faq-thematic/create/",
        FAQThematicViewSet.as_view({"post": "create"}),
        name="faq-thematic-create",
    ),
    path(
        "faq-thematic/<int:pk>",
        FAQThematicViewSet.as_view({"get": "retrieve"}),
        name="faq-thematic-detail",
    ),
    path(
        "faq-thematic/update/<int:pk>/",
        FAQThematicViewSet.as_view({"put": "update"}),
        name="faq-thematic-update",
    ),
    path(
        "faq-thematic/delete/<int:pk>/",
        FAQThematicViewSet.as_view({"delete": "destroy"}),
        name="faq-thematic-delete",
    ),
]
