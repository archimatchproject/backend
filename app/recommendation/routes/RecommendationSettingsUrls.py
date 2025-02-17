"""Exposed URLs for RecommendationSettings app.
ViewSet: RecommendationSettingsViewSet
"""

from django.urls import path

from app.recommendation.controllers.RecommendationSettingsViewSet import (
    RecommendationSettingsViewSet,
)


recommendation_settings_urlpatterns = [
    path(
        "settings/get-settings/<int:pk>",
        RecommendationSettingsViewSet.as_view({"get": "get_settings"}),
        name="get-settings",
    ),
    path(
        "settings/update-settings/<int:pk>",
        RecommendationSettingsViewSet.as_view({"put": "update_settings"}),
        name="update-settings",
    ),
    path(
        "settings/update-attributes/<int:pk>",
        RecommendationSettingsViewSet.as_view({"put": "update_attributes"}),
        name="update-attributes",
    ),
    path(
        "settings/get-settings-choices",
        RecommendationSettingsViewSet.as_view({"get": "get_settings_choices"}),
        name="get-settings-choices",
    ),
]
