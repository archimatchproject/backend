"""
Exposed URLs for the TermsAndConditions viewset.

This module defines the URL patterns for the TermsAndConditionsViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.cms.controllers.TermsAndConditionsViewSet import TermsAndConditionsViewSet


terms_and_conditions_urlpatterns = [
    path(
        "terms-and-conditions",
        TermsAndConditionsViewSet.as_view({"get": "list"}),
        name="terms-and-conditions-list",
    ),
    path(
        "terms-and-conditions/create/",
        TermsAndConditionsViewSet.as_view({"post": "create"}),
        name="terms-and-conditions-create",
    ),
    path(
        "terms-and-conditions/<int:pk>",
        TermsAndConditionsViewSet.as_view({"get": "retrieve"}),
        name="terms-and-conditions-detail",
    ),
    path(
        "terms-and-conditions/update/<int:pk>/",
        TermsAndConditionsViewSet.as_view({"put": "update"}),
        name="terms-and-conditions-update",
    ),
    path(
        "terms-and-conditions/delete/<int:pk>/",
        TermsAndConditionsViewSet.as_view({"delete": "destroy"}),
        name="terms-and-conditions-delete",
    ),
]
