"""
Serializer module for ProjectExtension model.

This module defines a serializer class for the ProjectExtension model.

"""

from rest_framework import serializers

from app.announcement.models.ProjectExtension import ProjectExtension


class ProjectExtensionSerializer(serializers.ModelSerializer):
    """
    Serializer class for ProjectExtension model.
    """

    class Meta:
        """
        Meta class for ProjectExtensionSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = ProjectExtension
        fields = ["id", "label", "icon", "property_type"]
