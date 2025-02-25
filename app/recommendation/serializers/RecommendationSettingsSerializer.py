"""
This module contains serializers for the RecommendationSettings model.
It includes both input and output serializers to handle the serialization
and deserialization of RecommendationSettings instances.

Classes:
    RecommendationSettingsInputSerializer: Serializer for creating and updating
    RecommendationSettings.
    RecommendationSettingsOutputSerializer: Serializer for retrieving RecommendationSettings
    details.
"""

from rest_framework import serializers

from app.recommendation import ARCHITECTURAL_STYLE_CHOICES
from app.recommendation import DISTANCE_LIMIT_CHOICES
from app.recommendation import DISTANCE_WEIGHT_CHOICES
from app.recommendation import NEEDS_PER_MATCH_CHOICES
from app.recommendation import NUM_RESULTS_CHOICES
from app.recommendation import ONGOING_PROJECTS_WEIGHT_CHOICES
from app.recommendation import PERFECT_MATCH_WEIGHT_CHOICES
from app.recommendation import PROJECT_CATEGORY_CHOICES
from app.recommendation import PROPERTY_TYPES_CHOICES
from app.recommendation import SCORE_PERCENTAGE_CHOICES
from app.recommendation import WORK_TYPE_CHOICES
from app.recommendation.models.AnnouncementWeights import AnnouncementWeights
from app.recommendation.models.RecommendationSettings import RecommendationSettings


# Input Serializer for RecommendationSettings
class RecommendationSettingsInputSerializer(serializers.ModelSerializer):
    """Input serializer for RecommendationSettings model."""

    attributes = serializers.PrimaryKeyRelatedField(queryset=AnnouncementWeights.objects.all())

    class Meta:
        """
        Meta class for the RecommendationSettingsSerializer.
        Attributes:
            model (RecommendationSettings): The model that is being serialized.
            fields (list): A list of fields to be included in the serialization. The fields are:
                - attributes: The attributes of the recommendation settings.
                - distance: The distance parameter for recommendations.
                - perfect_match: A flag indicating if a perfect match is required.
                - on_going_projects: The ongoing projects related to the recommendation settings.
                - distance_limit: The limit for the distance parameter.
                - score_percentage: The percentage score for recommendations.
                - num_results: The number of results to be returned.
        """

        model = RecommendationSettings
        fields = [
            "attributes",
            "distance",
            "perfect_match",
            "on_going_projects",
            "distance_limit",
            "score_percentage",
            "num_results",
        ]


# Output Serializer for RecommendationSettings
class RecommendationSettingsSerializer(serializers.ModelSerializer):
    """Serializer for RecommendationSettings with structured output, attributes, and choices."""

    settings = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the RecommendationSettingsSerializer.
        Attributes:
            model (RecommendationSettings): The model that is being serialized.
            fields (list): List of fields to be included in the serialization.
        """

        model = RecommendationSettings
        fields = ["id", "attributes", "settings"]

    def get_attributes(self, obj):
        """Generate structured output for recommendation attributes with choices."""
        return [
            {
                "name": "architectural_style",
                "label": "Architectural Style",
                "value": obj.attributes.architectural_style,
                "choices": ARCHITECTURAL_STYLE_CHOICES,
            },
            {
                "name": "work_type",
                "label": "Work Type",
                "value": obj.attributes.work_type,
                "choices": WORK_TYPE_CHOICES,
            },
            {
                "name": "project_category",
                "label": "Project Category",
                "value": obj.attributes.project_category,
                "choices": PROJECT_CATEGORY_CHOICES,
            },
            {
                "name": "property_type",
                "label": "Property Type",
                "value": obj.attributes.property_type,
                "choices": PROPERTY_TYPES_CHOICES,
            },
            {
                "name": "needs_per_match",
                "label": "Needs per Match",
                "value": obj.attributes.needs_per_match,
                "choices": NEEDS_PER_MATCH_CHOICES,
            },
        ]

    def get_settings(self, obj):
        """Generate structured output for recommendation settings with choices."""
        return [
            {
                "name": "distance",
                "label": "Distance Weight",
                "value": obj.distance,
                "choices": DISTANCE_WEIGHT_CHOICES,
            },
            {
                "name": "perfect_match",
                "label": "Perfect Match Weight",
                "value": obj.perfect_match,
                "choices": PERFECT_MATCH_WEIGHT_CHOICES,
            },
            {
                "name": "on_going_projects",
                "label": "Ongoing Projects Weight",
                "value": obj.on_going_projects,
                "choices": ONGOING_PROJECTS_WEIGHT_CHOICES,
            },
            {
                "name": "distance_limit",
                "label": "Distance Limit (km)",
                "value": obj.distance_limit,
                "choices": DISTANCE_LIMIT_CHOICES,
            },
            {
                "name": "score_percentage",
                "label": "Minimum Score Percentage",
                "value": obj.score_percentage,
                "choices": SCORE_PERCENTAGE_CHOICES,
            },
            {
                "name": "num_results",
                "label": "Number of Results",
                "value": obj.num_results,
                "choices": NUM_RESULTS_CHOICES,
            },
        ]
