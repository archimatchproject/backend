"""
exposed URLS for announcement app
viewset : AnnouncementViewSet
"""

from django.urls import path

from app.selection.controllers.SelectionSettingsViewSet import SelectionSettingsViewSet


selectionSettings_urlpatterns = [
    path(
        "settings/get-settings/<int:pk>",
        SelectionSettingsViewSet.as_view({"get": "get_settings"}),
        name="get-settings",
    ),
    path(
        "settings/update-settings/<int:pk>",
        SelectionSettingsViewSet.as_view({"put": "update_settings"}),
        name="update-settings",
    ),
    path(
        "settings/get-settings-choices",
        SelectionSettingsViewSet.as_view({"get": "get_settings_choices"}),
        name="get-settings-choices",
    ),
]
