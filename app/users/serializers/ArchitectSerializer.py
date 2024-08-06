"""
Module containing ArchitectSerializer class.

This module provides a serializer for the Architect model, including nested serialization for the
 ArchimatchUser model.

Classes:
    ArchitectSerializer: Serializer for the Architect model with nested ArchimatchUser.
    ArchitectBaseDetailsSerializer: Serializer for the base details of the Architect model.
    ArchitectCompanyDetailsSerializer: Serializer for the company details of the Architect model.
"""

from rest_framework import serializers

from app.announcement.models.Need import Need
from app.announcement.serializers.ArchitectSpecialitySerializer import ArchitectSpecialitySerializer
from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.NeedSerializer import NeedSerializer
from app.announcement.serializers.ProjectCategorySerializer import ProjectCategorySerializer
from app.announcement.serializers.PropertyTypeSerializer import PropertyTypeSerializer
from app.announcement.serializers.WorkTypeSerializer import WorkTypeSerializer
from app.core.models.Budget import Budget
from app.core.models.PreferredLocation import PreferredLocation
from app.core.models.PropertyType import PropertyType
from app.core.models.TerrainSurface import TerrainSurface
from app.core.models.WorkSurface import WorkSurface
from app.core.models.WorkType import WorkType
from app.core.serializers.BudgetSerializer import BudgetSerializer
from app.core.serializers.PreferredLocationSerializer import PreferredLocationSerializer
from app.core.serializers.TerrainSurfaceSerializer import TerrainSurfaceSerializer
from app.core.serializers.WorkSurfaceSerializer import WorkSurfaceSerializer
from app.subscription.serializers.SelectedSubscriptionPlanSerializer import (
    SelectedSubscriptionPlanSerializer,
)
from app.users.models.Architect import Architect
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class ArchitectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Architect model.

    This serializer includes nested serialization for the ArchimatchUser model and manages
    architect-specific fields.

    Fields:
        user: Nested serializer for the ArchimatchUser associated with the architect.
        architectural_styles: Nested serializer for architectural styles.
        project_categories: Nested serializer for project categories.
        property_types: Nested serializer for property types.
        work_types: Nested serializer for work types.
        architect_speciality: Nested serializer for architect speciality.
        needs: Nested serializer for needs.
    """

    user = ArchimatchUserSerializer(required=True)
    architectural_styles = ArchitecturalStyleSerializer(many=True)
    project_categories = ProjectCategorySerializer(many=True)
    property_types = PropertyTypeSerializer(many=True)
    work_types = WorkTypeSerializer(many=True)
    architect_speciality = ArchitectSpecialitySerializer()
    needs = NeedSerializer(many=True)
    subscription_plan = SelectedSubscriptionPlanSerializer()
    terrain_surfaces = TerrainSurfaceSerializer(many=True,required=False)
    work_surfaces = WorkSurfaceSerializer(many=True,required=False)
    preferred_locations = PreferredLocationSerializer(many=True,required=False)
    budgets = BudgetSerializer(many=True,required=False)

    class Meta:
        """
        Meta class for ArchitectSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Architect
        fields = "__all__"


class ArchitectBaseDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the base details of the Architect model.

    This serializer includes nested serialization for the ArchimatchUser model.

    Fields:
        first_name: First name from the ArchimatchUser associated with the Architect.
        last_name: Last name from the ArchimatchUser associated with the Architect.
        phone_number: Phone number from the ArchimatchUser associated with the Architect.
        email: Email from the ArchimatchUser associated with the Architect.
        bio: Bio of the Architect.
        presentation_video: Presentation video of the Architect.
    """

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone_number = serializers.CharField(source="user.phone_number")
    email = serializers.CharField(source="user.email")

    class Meta:
        """
        Meta class for ArchitectBaseDetailsSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Architect
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "bio",
            "presentation_video",
        )


class ArchitectCompanyDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the company details of the Architect model.

    Fields:
        company_name: Name of the company associated with the Architect.
        company_logo: Logo of the company associated with the Architect.
        architect_identifier: Identifier for the Architect.
    """

    class Meta:
        """
        Meta class for ArchitectCompanyDetailsSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Architect
        fields = (
            "id",
            "company_name",
            "company_logo",
            "architect_identifier",
        )


class ArchitectUpdatePreferencesSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Architect preferences.

    This serializer handles nested serialization for many-to-many relationships
    such as project categories, property types, work types, and architectural styles.

    Fields:
        project_categories: List of primary keys for associated project categories.
        property_types: List of primary keys for associated property types.
        work_types: List of primary keys for associated work types.
        architectural_styles: List of primary keys for associated architectural styles.
    """

    property_types = serializers.PrimaryKeyRelatedField(
        queryset=PropertyType.objects.all(), many=True
    )
    work_types = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all(), many=True)
    terrain_surfaces = serializers.PrimaryKeyRelatedField(
        queryset=TerrainSurface.objects.all(), many=True
    )
    work_surfaces = serializers.PrimaryKeyRelatedField(
        queryset=WorkSurface.objects.all(), many=True
    )
    preferred_locations = serializers.PrimaryKeyRelatedField(
        queryset=PreferredLocation.objects.all(), many=True
    )
    budgets = serializers.PrimaryKeyRelatedField(queryset=Budget.objects.all(), many=True)
    needs = serializers.PrimaryKeyRelatedField(queryset=Need.objects.all(), many=True)

    class Meta:
        """
        Meta class for ArchitectUpdatePreferencesSerializer.

        Attributes:
            model: The model that this serializer is associated with (Architect).
            fields: The fields to include in the serialized representation.
        """

        model = Architect
        fields = [
            "preferred_locations",
            "property_types",
            "work_types",
            "terrain_surfaces",
            "work_surfaces",
            "budgets",
            "needs",
        ]
