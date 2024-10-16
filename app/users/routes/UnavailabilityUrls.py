"""
exposed URLS for users app
viewset : ClientViewSet
"""

from django.urls import path

from app.users.controllers.UnavailabilityViewSet import UnavailabilityViewSet


unavailability_urlpatterns = [
    path(
        "unavailability/create/",
        UnavailabilityViewSet.as_view({"post": "create"}),
        name="create",
    ),
    path(
        "unavailability/get-available-time-slots/",
        UnavailabilityViewSet.as_view({"get": "get_available_time_slots"}),
        name="get-available-time-slots",
    ),
    
]
