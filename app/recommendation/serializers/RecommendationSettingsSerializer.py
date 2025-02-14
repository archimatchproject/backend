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
from app.recommendation import (
    ARCHITECTURAL_STYLE_CHOICES,
    DISTANCE_LIMIT_CHOICES,
    DISTANCE_WEIGHT_CHOICES,
    NUM_RESULTS_CHOICES,
    ONGOING_PROJECTS_WEIGHT_CHOICES,
    PERFECT_MATCH_WEIGHT_CHOICES,
    PROJECT_CATEGORY_CHOICES,
    SCORE_PERCENTAGE_CHOICES,
    WORK_TYPE_CHOICES,
    PROPERTY_TYPES_CHOICES,
    NEEDS_PER_MATCH_CHOICES,
)
from app.recommendation.models.RecommendationSettings import RecommendationSettings
from app.recommendation.models.AnnouncementWeights import AnnouncementWeights


# Input Serializer for RecommendationSettings
class RecommendationSettingsInputSerializer(serializers.ModelSerializer):
    """Input serializer for RecommendationSettings model."""

    attributes = serializers.PrimaryKeyRelatedField(
        queryset=AnnouncementWeights.objects.all()
    )

    class Meta:
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
                "name": "property_types",
                "label": "Property Types",
                "value": obj.attributes.property_types,
                "choices": PROPERTY_TYPES_CHOICES,
            },
            {
                "name": "needs_per_match_weight",
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
                "name": "on_going_projectst",
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
