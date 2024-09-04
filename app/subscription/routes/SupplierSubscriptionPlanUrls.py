"""
Exposed URLs for the SubscriptionPlan model.

This module defines the URL patterns for the SubscriptionPlanViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.subscription.controllers.SupplierSubscriptionPlanViewSet import SupplierSubscriptionPlanViewSet


supplier_subscription_plan_urlpatterns = [
    path(
        "subscription-plan",
        SupplierSubscriptionPlanViewSet.as_view({"get": "list"}),
        name="subscription-plan-list",
    ),
    path(
        "subscription-plan/create/",
        SupplierSubscriptionPlanViewSet.as_view({"post": "create"}),
        name="subscription-plan-create",
    ),
    path(
        "subscription-plan/<int:pk>",
        SupplierSubscriptionPlanViewSet.as_view({"get": "retrieve"}),
        name="subscription-plan-detail",
    ),
    path(
        "subscription-plan/update/<int:pk>/",
        SupplierSubscriptionPlanViewSet.as_view({"put": "update"}),
        name="subscription-plan-update",
    ),
    path(
        "subscription-plan/delete/<int:pk>/",
        SupplierSubscriptionPlanViewSet.as_view({"delete": "destroy"}),
        name="subscription-plan-delete",
    ),
    path(
        "subscription-plan/upgradable-plans/",
        SupplierSubscriptionPlanViewSet.as_view({"get": "get_upgradable_plans"}),
        name="upgradable-plans",
    ),
]
