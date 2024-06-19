from rest_framework import serializers

from app.announcement.models.utils.Need import Need


class NeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Need
        fields = ["id", "label", "icon", "architect_speciality"]
