"""
exposed URLS for architect_realization app
viewset : Realization viewset
"""

from django.urls import path

from app.architect_realization.controllers.RealizationViewSet import RealizationViewSet


architect_realization_urlpatterns = [
    path(
        "create-realization/",
        RealizationViewSet.as_view({"post": "realization_create"}),
        name="create-realization",
    ),
    path(
        "all-realizations/",
        RealizationViewSet.as_view({"get": "get"}),
        name="get-all-realizations",
    ),
    path(
        "architectural-styles/",
        RealizationViewSet.as_view({"get": "get_architectural_styles"}),
        name="architectural-styles",
    ),
    path(
        "needs/",
        RealizationViewSet.as_view({"get": "get_needs"}),
        name="needs",
    ),
    path(
        "get-realizations-by-category/<int:pk>/",
        RealizationViewSet.as_view({"get": "get_realizations_by_category"}),
        name="get-realizations-by-category",
    ),
    path(
        "details/<int:pk>/",
        RealizationViewSet.as_view({"get": "retrieve"}),
        name="get",
    ),
    path(
        "get-realizations-by-architect/<int:pk>/",
        RealizationViewSet.as_view({"get": "get_realizations_by_architect"}),
        name="get-realizations-by-architect",
    ),
    path(
        "delete/<int:pk>/",
        RealizationViewSet.as_view({"delete": "destroy"}),
        name="delete",
    ),
    path(
        "update-realization-images/<int:pk>/",
        RealizationViewSet.as_view({"put": "update_realization_images"}),
        name="update-realization-images",
    ),
    path(
        "get-realizations/",
        RealizationViewSet.as_view({"get": "get_realizations"}),
        name="get-realizations",
    ),
        path(
        "get-architect-realizations/",
        RealizationViewSet.as_view({"get": "get_architect_realizations"}),
        name="get-architect-realizations",
    ),
]
