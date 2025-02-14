"""Service module for RecommendationSettings operations.

This module defines the `RecommendationSettingsService` class, which handles operations
related to `RecommendationSettings`, such as retrieving, updating, and listing available choices,
as well as updating attribute settings.
"""

from rest_framework.exceptions import ValidationError, APIException
from django.db import transaction
from app.recommendation.models.AnnouncementWeights import AnnouncementWeights
from app.recommendation.models.RecommendationSettings import RecommendationSettings
from app.recommendation.serializers.RecommendationSettingsSerializer import (
    RecommendationSettingsSerializer,
)
from app.recommendation.serializers.AnnouncementWeightsSerializer import (
    AnnouncementWeightsSerializer,
)
from app.recommendation import (
    ARCHITECTURAL_STYLE_CHOICES,
    WORK_TYPE_CHOICES,
    PROJECT_CATEGORY_CHOICES,
    PROPERTY_TYPES_CHOICES,
    NEEDS_PER_MATCH_CHOICES,
    DISTANCE_WEIGHT_CHOICES,
    PERFECT_MATCH_WEIGHT_CHOICES,
    ONGOING_PROJECTS_WEIGHT_CHOICES,
    DISTANCE_LIMIT_CHOICES,
    SCORE_PERCENTAGE_CHOICES,
    NUM_RESULTS_CHOICES,
)


class RecommendationSettingsService:
    """Service class for handling operations related to `RecommendationSettings`."""

    @classmethod
    def get_recommendation_settings(cls, pk: int) -> tuple:
        """Retrieve the recommendation settings.

        Args:
            pk (int): The primary key of the recommendation settings instance.

        Returns:
            tuple: A tuple containing a success flag (bool) and the serialized recommendation
            settings data (dict).
        """
        try:
            settings = RecommendationSettings.objects.get(id=pk)
        except RecommendationSettings.DoesNotExist:
            raise APIException("Recommendation settings not configured.")

        serializer = RecommendationSettingsSerializer(settings)
        return True, serializer.data

    @classmethod
    @transaction.atomic
    def update_recommendation_settings(cls, data: dict, pk: int) -> tuple:
        """Update a specific recommendation setting.

        Args:
            data (dict): A dictionary containing the field name (`name`) and its updated value
            (`value`).
            pk (int): The primary key of the recommendation settings instance.

        Returns:
            tuple: A tuple containing a success flag (bool) and the updated serialized
            recommendation settings data (dict).
        """
        try:
            settings = RecommendationSettings.objects.get(id=pk)
        except RecommendationSettings.DoesNotExist:
            raise APIException("Recommendation settings not configured.")

        field_name = data.get("name")
        new_value = data.get("value")

        if not hasattr(settings, field_name):
            raise ValidationError(
                detail=f"Field '{field_name}' does not exist in RecommendationSettings."
            )

        setattr(settings, field_name, new_value)
        settings.full_clean()
        settings.save()

        serializer = RecommendationSettingsSerializer(settings)
        return True, serializer.data

    @classmethod
    @transaction.atomic
    def update_recommendation_attributes(cls, data: dict, pk: int) -> tuple:
        """Update attributes within the recommendation settings.

        Args:
            data (dict): A dictionary containing the attribute field name (`name`) and its updated
            value (`value`).
            pk (int): The primary key of the recommendation settings instance.

        Returns:
            tuple: A tuple containing a success flag (bool) and the updated serialized attributes
            data (dict).
        """
        try:
            settings = RecommendationSettings.objects.get(id=pk)
            attributes = settings.attributes
        except (RecommendationSettings.DoesNotExist, AnnouncementWeights.DoesNotExist):
            raise APIException("Recommendation attributes not configured.")

        field_name = data.get("name")
        new_value = data.get("value")

        if not hasattr(attributes, field_name):
            raise ValidationError(
                detail=f"Field '{field_name}' does not exist in AnnouncementWeights."
            )

        setattr(attributes, field_name, new_value)
        attributes.full_clean()
        attributes.save()

        serializer = AnnouncementWeightsSerializer(attributes)
        return True, serializer.data

    @classmethod
    def get_recommendation_settings_choices(cls) -> tuple:
        """Retrieve the recommendation settings choices.

        Returns:
            tuple: A tuple containing a success flag (bool) and a dictionary of available choices
            for each setting.
        """
        data = {
            "architectural_style": ARCHITECTURAL_STYLE_CHOICES,
            "work_type": WORK_TYPE_CHOICES,
            "project_category": PROJECT_CATEGORY_CHOICES,
            "property_types": PROPERTY_TYPES_CHOICES,
            "needs_per_match_weight": NEEDS_PER_MATCH_CHOICES,
            "distance_weight": DISTANCE_WEIGHT_CHOICES,
            "perfect_match_weight": PERFECT_MATCH_WEIGHT_CHOICES,
            "on_going_projects_weight": ONGOING_PROJECTS_WEIGHT_CHOICES,
            "distance_limit": DISTANCE_LIMIT_CHOICES,
            "score_percentage": SCORE_PERCENTAGE_CHOICES,
            "num_results": NUM_RESULTS_CHOICES,
        }
        return True, data
