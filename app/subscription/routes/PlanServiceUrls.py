"""
Exposed URLs for the PlanService model.

This module defines the URL patterns for the PlanServiceViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.subscription.controllers.PlanServiceViewSet import PlanServiceViewSet


plan_service_urlpatterns = [
    path(
        "plan-service",
        PlanServiceViewSet.as_view({"get": "list"}),
        name="plan-service-list",
    ),
    path(
        "plan-service/create/",
        PlanServiceViewSet.as_view({"post": "create"}),
        name="plan-service-create",
    ),
    path(
        "plan-service/<int:pk>",
        PlanServiceViewSet.as_view({"get": "retrieve"}),
        name="plan-service-detail",
    ),
    path(
        "plan-service/update/<int:pk>/",
        PlanServiceViewSet.as_view({"put": "update"}),
        name="plan-service-update",
    ),
    path(
        "plan-service/delete/<int:pk>/",
        PlanServiceViewSet.as_view({"delete": "destroy"}),
        name="plan-service-delete",
    ),
]
