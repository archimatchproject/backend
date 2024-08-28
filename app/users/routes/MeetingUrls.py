"""
exposed URLS for users app
viewset : MeetingViewSet
"""

from django.urls import path

from app.users.controllers.MeetingViewSet import MeetingViewSet


meeting_urlpatterns = [
    path(
        "meeting/create/",
        MeetingViewSet.as_view({"post": "create"}),
        name="create",
    ),
    path(
        "meeting/admin-meetings/",
        MeetingViewSet.as_view({"get": "get_admin_meetings"}),
        name="admin-meetings",
    ),
]
