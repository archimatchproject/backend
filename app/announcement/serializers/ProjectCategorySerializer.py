"""
Serializer module for ProjectCategory model.

This module defines a serializer class for the ProjectCategory model.
"""

from rest_framework import serializers

from app.core.models.ProjectCategory import ProjectCategory


class ProjectCategorySerializer(serializers.ModelSerializer):
    """
    Serializer class for ProjectCategory model.
    """

    class Meta:
        """
        Meta class for ProjectCategorySerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = ProjectCategory
        fields = ["id", "label", "icon"]
