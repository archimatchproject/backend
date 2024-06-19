from rest_framework import serializers

from app.announcement.models.utils.AnnouncementWorkType import AnnouncementWorkType


class AnnouncementWorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementWorkType
        fields = ["id", "header", "description"]
