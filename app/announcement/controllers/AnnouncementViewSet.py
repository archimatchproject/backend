from rest_framework import viewsets

from app.announcement.models import Announcement
from app.announcement.serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Announcement instances.
    """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
