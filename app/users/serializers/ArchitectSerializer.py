"""
Module containing ArchitectSerializer class.

This module provides a serializer for the Architect model, including nested serialization for the
 ArchimatchUser model.

Classes:
    ArchitectSerializer: Serializer for the Architect model with nested ArchimatchUser.
"""

from rest_framework import serializers

from app.announcement.serializers.ArchitectSpecialitySerializer import ArchitectSpecialitySerializer
from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.ProjectCategorySerializer import ProjectCategorySerializer
from app.announcement.serializers.PropertyTypeSerializer import PropertyTypeSerializer
from app.announcement.serializers.WorkTypeSerializer import WorkTypeSerializer
from app.users.models import Architect
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class ArchitectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Architect model.

    This serializer includes nested serialization for the ArchimatchUser model and manages
    architect-specific fields.

    Fields:
        user: Nested serializer for the ArchimatchUser associated with the architect.
    """

    user = ArchimatchUserSerializer(required=True)
    architectural_styles = ArchitecturalStyleSerializer(many=True)
    project_categories = ProjectCategorySerializer(many=True)
    property_types = PropertyTypeSerializer(many=True)
    work_types = WorkTypeSerializer(many=True)
    architect_speciality = ArchitectSpecialitySerializer()

    class Meta:
        """
        Meta class for ArchitectSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Architect
        fields = "__all__"
