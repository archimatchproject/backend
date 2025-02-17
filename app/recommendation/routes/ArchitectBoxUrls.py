"""
exposed URLS for announcement app
viewset : AnnouncementViewSet
"""

from django.urls import path

from app.recommendation.controllers.ArchitectBoxViewSet import ArchitectBoxViewSet


box_urlpatterns = [
    path(
        "get-architect-score/<int:pk>",
        ArchitectBoxViewSet.as_view({"post": "get_architect_score"}),
        name="get-architect-score",
    ),
    path(
        "get-box-announcements",
        ArchitectBoxViewSet.as_view({"get": "get_box_announcements"}),
        name="get-box-announcements",
    ),
]
