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
    path(
        "get-selection/<int:pk>",
        SelectionViewSet.as_view({"get": "retrieve"}),
        name="get-selection",
    ),
    path(
        "get-announcement-selections/<int:pk>",
        SelectionViewSet.as_view({"get": "get_announcement_selections"}),
        name="get-announcement-selections",
    ),
    path(
        "get-architect-selections/",
        SelectionViewSet.as_view({"get": "get_architect_selections"}),
        name="get-architect-selections",
    ),
    path(
        "update-name/<int:pk>",
        SelectionViewSet.as_view({"put": "update_selection_name"}),
        name="update-name",
    ),
    path(
        "confirm-discussion-phase/<int:pk>",
        SelectionViewSet.as_view({"post": "confirm_discussion_phase"}),
        name="confirm-discussion-phase",
    ),
]
