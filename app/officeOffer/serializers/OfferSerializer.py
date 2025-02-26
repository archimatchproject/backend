"""
Module defining the serializer for the Offer model.

This module contains the OfferSerializer class, which serializes the data
for creating or updating a job offer in the application.
"""

from rest_framework import serializers

from app.announcement.serializers.ArchitectSpecialitySerializer import ArchitectSpecialitySerializer
from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.ProjectCategorySerializer import ProjectCategorySerializer
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.models.ProjectCategory import ProjectCategory
from app.officeOffer import EXPERIENCE_CHOICES
from app.officeOffer.models import Offer
from app.officeOffer.models.SoftwareSkill import SoftwareSkill
from app.officeOffer.models.TechnicalSkill import TechnicalSkill
from app.officeOffer.serializers.SoftwareSkillSerializer import SoftwareSkillSerializer
from app.officeOffer.serializers.TechnicalSkillSerializer import TechnicalSkillSerializer
from app.users.models.Office import Office


class OfferPOSTSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offer model.

    This class defines the structure for serializing the Offer model data,
    including validation and nested relations for creating or updating an offer.
    """

    architect_speciality = serializers.PrimaryKeyRelatedField(queryset=ArchitectSpeciality.objects.all())
    project_category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    architectural_style = serializers.PrimaryKeyRelatedField(queryset=ArchitecturalStyle.objects.all(), required=False)
    technical_skills = serializers.PrimaryKeyRelatedField(
        queryset=TechnicalSkill.objects.all(), many=True, required=False
    )
    software_skills = serializers.PrimaryKeyRelatedField(
        queryset=SoftwareSkill.objects.all(), many=True, required=False
    )

    class Meta:
        """
        Meta class for OfferPOSTSerializer.

        Defines the model to be serialized (`Offer`) and the fields that should be included
        in the serialized data. Fields include relationships (ForeignKeys and ManyToManyFields)
        as well as additional attributes like the offer title, contract type, and description.
        """

        model = Offer
        fields = [
            "architect_speciality",
            "offer_title",
            "contract_type",
            "contract_duration",
            "work_location",
            "start_date",
            "salary_range",
            "project_category",
            "architectural_style",
            "office_description",
            "offer_description",
            "searched_profile",
            "technical_skills",
            "software_skills",
            "experience_required",
        ]

    def validate_experience_required(self, value):
        """
        Custom validation for the 'experience_required' field.
        """
        if value and value not in dict(EXPERIENCE_CHOICES).keys():
            raise serializers.ValidationError("Invalid experience required value.")
        return value


class OfferPUTSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing Offer instances.

    This serializer handles the PUT validation and updating logic for Offer instances.
    """

    office = serializers.PrimaryKeyRelatedField(queryset=Office.objects.all())
    architect_speciality = serializers.PrimaryKeyRelatedField(queryset=ArchitectSpeciality.objects.all())
    project_category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    architectural_style = serializers.PrimaryKeyRelatedField(queryset=ArchitecturalStyle.objects.all(), required=False)
    technical_skills = serializers.PrimaryKeyRelatedField(
        queryset=TechnicalSkill.objects.all(), many=True, required=False
    )
    software_skills = serializers.PrimaryKeyRelatedField(
        queryset=SoftwareSkill.objects.all(), many=True, required=False
    )

    class Meta:
        """
        Meta class for OfferPUTSerializer.

        Defines the model to be serialized (`Offer`) and the fields that should be included
        in the serialized data. This serializer is used for PUT requests to update existing
        Offer instances.
        """

        model = Offer
        fields = [
            "architect_speciality",
            "offer_title",
            "contract_type",
            "contract_duration",
            "work_location",
            "start_date",
            "salary_range",
            "office",
            "project_category",
            "architectural_style",
            "office_description",
            "offer_description",
            "searched_profile",
            "technical_skills",
            "software_skills",
            "experience_required",
        ]

    def validate_experience_required(self, value):
        """
        Custom validation for the 'experience_required' field.
        """
        if value and value not in dict(EXPERIENCE_CHOICES).keys():
            raise serializers.ValidationError("Invalid experience required value.")
        return value


class OfferOutputSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving Offer instances.

    This serializer transforms the Offer instance data into a readable format for the client.
    """

    architect_speciality = ArchitectSpecialitySerializer()
    architectural_style = ArchitecturalStyleSerializer()
    project_category = ProjectCategorySerializer()
    technical_skills = TechnicalSkillSerializer(many=True)
    software_skills = SoftwareSkillSerializer(many=True)

    class Meta:
        """
        Meta class for OfferOutputSerializer.

        Defines the model to be serialized (`Offer`) and the fields that should be included
        in the output data. This serializer is used for retrieving and displaying Offer
        instances, including related data such as office, architectural styles, and skills.
        """

        model = Offer
        fields = [
            "id",
            "office",
            "architect_speciality",
            "offer_title",
            "contract_type",
            "contract_duration",
            "work_location",
            "start_date",
            "salary_range",
            "project_category",
            "architectural_style",
            "office_description",
            "offer_description",
            "searched_profile",
            "technical_skills",
            "software_skills",
            "experience_required",
        ]
