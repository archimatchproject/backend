from rest_framework import viewsets

from app.announcement.models import Announcement
from app.announcement.serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
