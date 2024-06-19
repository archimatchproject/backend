from rest_framework import serializers

from app.announcement.models.utils.ProjectImage import ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["id", "image"]
