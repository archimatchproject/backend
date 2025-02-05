"""
exposed URLS for announcement app
viewset : AnnouncementViewSet
"""

from django.urls import path

from app.selection.controllers.QuoteViewSet import QuoteViewSet


quote_urlpatterns = [
    path(
        "create-quote/<int:pk>",
        QuoteViewSet.as_view({"post": "create_quote"}),
        name="create-selection",
    ),
    path(
        "accept-quote/<int:pk>",
        QuoteViewSet.as_view({"put": "accept_quote"}),
        name="create-selection",
    ),
    path(
        "refuse-quote/<int:pk>",
        QuoteViewSet.as_view({"put": "refuse_quote"}),
        name="create-selection",
    ),
    path(
        "delete-quote/<int:pk>",
        QuoteViewSet.as_view({"delete": "destroy"}),
        name="delete-quote",
    ),
]
