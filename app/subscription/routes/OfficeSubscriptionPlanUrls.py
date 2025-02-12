"""
Exposed URLs for the OfficeSubscriptionPlan model.

This module defines the URL patterns for the OfficeSubscriptionPlanViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.subscription.controllers.OfficeSubscriptionPlanViewSet import OfficeSubscriptionPlanViewSet


office_subscription_plan_urlpatterns = [
    path(
        "office-subscription-plan",
        OfficeSubscriptionPlanViewSet.as_view({"get": "list"}),
        name="office-subscription-plan-list",
    ),
    path(
        "office-subscription-plan/create/",
        OfficeSubscriptionPlanViewSet.as_view({"post": "create"}),
        name="office-subscription-plan-create",
    ),
    path(
        "office-subscription-plan/<int:pk>",
        OfficeSubscriptionPlanViewSet.as_view({"get": "retrieve"}),
        name="office-subscription-plan-detail",
    ),
    path(
        "office-subscription-plan/update/<int:pk>/",
        OfficeSubscriptionPlanViewSet.as_view({"put": "update"}),
        name="office-subscription-plan-update",
    ),
    path(
        "office-subscription-plan/delete/<int:pk>/",
        OfficeSubscriptionPlanViewSet.as_view({"delete": "destroy"}),
        name="office-subscription-plan-delete",
    ),
    path(
        "office-subscription-plan/upgradable-plans/",
        OfficeSubscriptionPlanViewSet.as_view({"get": "get_upgradable_plans"}),
        name="upgradable-office-plans",
    ),
]
