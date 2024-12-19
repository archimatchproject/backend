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
    path(
        "delete-selection/<int:pk>",
        SelectionViewSet.as_view({"delete": "destroy"}),
        name="delete-selection",
    ),
    path(
        "get-selections-paginated/",
        SelectionViewSet.as_view({"get": "get"}),
        name="get-selections-paginated",
    ),
    path(
        "abandon-selection/<int:pk>",
        SelectionViewSet.as_view({"put": "abandon_selection"}),
        name="abandon-selection",
    ),
    path(
        "not-selected-announcements/",
        SelectionViewSet.as_view({"get": "get_not_selected_announcements"}),
        name="not-selected-announcements",
    ),
        path(
        "broadcast-announcement/<int:pk>",
        SelectionViewSet.as_view({"post": "broadcast_announcement"}),
        name="broadcast-announcement",
    ),
    path(
        "get-discussion-phase-selections/",
        SelectionViewSet.as_view({"get": "get_discussion_phase_selections"}),
        name="get-discussion-phase-selections",
    ),
    path(
        "selection-logs/<int:pk>",
        SelectionViewSet.as_view({"get": "get_selection_logs"}),
        name="selection-logs",
    ),
    path(
        "broadcast-selection-announcement/<int:pk>",
        SelectionViewSet.as_view({"post": "broadcast_selection_announcement"}),
        name="broadcast-selection-announcement",
    ),
    path(
        "block-selection/<int:pk>",
        SelectionViewSet.as_view({"post": "block_selection"}),
        name="block-selection",
    ),
    path(
        "change-selection-deadline/<int:pk>",
        SelectionViewSet.as_view({"post": "change_selection_deadline"}),
        name="change-selection-deadline",
    ),
    path(
        "confirm-discussion-phase-admin/<int:pk>",
        SelectionViewSet.as_view({"post": "confirm_discussion_phase_admin"}),
        name="confirm-discussion-phase-admin",
    ),
    path(
        "cancel-selection/<int:pk>",
        SelectionViewSet.as_view({"post": "cancel_selection"}),
        name="cancel-selection",
    ),
    path(
        "get-quote-phase-selections/",
        SelectionViewSet.as_view({"get": "get_quote_phase_selections"}),
        name="get-quote-phase-selections",
    ),
]
