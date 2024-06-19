from rest_framework import serializers

from app.announcement.models.utils.ProjectCategory import ProjectCategory


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ["id", "label", "icon"]
