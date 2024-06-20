"""
Serializer module for ProjectImage model.

This module defines a serializer class for the ProjectImage model.

"""

from rest_framework import serializers

from app.announcement.models.ProjectImage import ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    """
    Serializer class for ProjectImage model.
    """

    class Meta:
        """
        Meta class for ProjectImageSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = ProjectImage
        fields = ["id", "image"]
