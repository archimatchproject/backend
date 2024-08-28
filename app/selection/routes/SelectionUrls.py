"""
exposed URLS for announcement app
viewset : AnnouncementViewSet
"""

from django.urls import path

from app.selection.controllers.SelectionViewSet import SelectionViewSet


selection_urlpatterns = [
    path(
        "create-selection",
        SelectionViewSet.as_view({"post": "create"}),
        name="create-selection",
    ),
]
