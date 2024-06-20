"""
Module for Announcement ViewSet.

This module defines the AnnouncementViewSet class, which is a viewset
for viewing and editing Announcement instances using Django REST Framework.
"""

from rest_framework import viewsets

from app.announcement.models import Announcement
from app.announcement.serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Announcement model.

    Provides endpoints for viewing and editing Announcement instances.
    """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
