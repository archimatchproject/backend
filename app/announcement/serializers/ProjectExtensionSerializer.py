from rest_framework import serializers

from app.announcement.models.ProjectExtension import ProjectExtension


class ProjectExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectExtension
        fields = ["id", "label", "icon"]
