"""
exposed URLS for announcement app
viewset : AnnouncementViewSet
"""

from django.urls import path

from app.recommendation.controllers.ArchitectBoxViewSet import (
    ArchitectBoxViewSet,
)


box_urlpatterns = [
    path(
        "get-announcements",
        ArchitectBoxViewSet.as_view({"get": "get"}),
        name="get-announcements",
    ),
    path(
        "get-box-announcements",
        ArchitectBoxViewSet.as_view({"get": "get_box_announcements"}),
        name="get-box-announcements",
    ),
]
