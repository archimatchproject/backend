"""
exposed URLS for announcement app
viewset : AnnouncementViewSet
"""

from django.urls import path

from app.selection.controllers.QuoteViewSet import QuoteViewSet


quote_urlpatterns = [
    path(
        "create-quote",
        QuoteViewSet.as_view({"post": "create_quote"}),
        name="create-selection",
    ),
    path(
        "accept-quote",
        QuoteViewSet.as_view({"put": "accept_quote"}),
        name="create-selection",
    ),
    path(
        "refuse-quote",
        QuoteViewSet.as_view({"post": "refuse_quote"}),
        name="create-selection",
    ),
]
