from rest_framework import serializers

from app.announcement.models.utils.ArchitectSpeciality import ArchitectSpeciality


class ArchitectSpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchitectSpeciality
        fields = ["id", "label", "icon"]
