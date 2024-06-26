"""
Module containing the viewset for the Meeting model.

This module defines the viewset for the Meeting model to provide
CRUD operations and additional functionality through the API.

Classes:
    MeetingViewSet: Viewset for the Meeting model.
"""

from rest_framework import viewsets

from app.architect_request.models.Meeting import Meeting
from app.architect_request.serializers.MeetingSerializer import MeetingSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    """
    Viewset for the Meeting model.

    Provides CRUD operations and additional functionality for Meeting instances.

    Attributes:
        queryset (QuerySet): The queryset of Meeting instances.
        serializer_class (MeetingSerializer): The serializer class for Meeting instances.
    """

    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
