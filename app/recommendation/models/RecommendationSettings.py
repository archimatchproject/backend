"""
This module defines the RecommendationSettings model, a singleton model for managing general
recommendation settings.
Classes:
    RecommendationSettings: A Django model representing the settings for recommendations,
    ensuring only one instance exists.
"""

from django.db import models

from rest_framework.exceptions import ValidationError

from app.recommendation.models.AnnouncementWeights import AnnouncementWeights


class RecommendationSettings(models.Model):
    """Singleton model for managing general recommendation settings.

    Attributes:
        attributes (AnnouncementWeights): Relation to AnnouncementWeights containing attribute
        weights.
        distance (int): Weight for distance calculation.
        perfect_match (int): Weight for perfect match score.
        on_going_projects (int): Weight for ongoing projects penalty.
        distance_limit (int): Maximum allowed distance for recommendations (in km).
        score_percentage (int): Minimum score percentage threshold for recommendations.
        num_results (int): Number of results to return for recommendations.
    """

    attributes = models.OneToOneField(
        AnnouncementWeights, on_delete=models.CASCADE, related_name="settings"
    )
    distance = models.IntegerField(default=25)
    perfect_match = models.IntegerField(default=5)
    on_going_projects = models.IntegerField(default=5)
    distance_limit = models.IntegerField(default=200)
    score_percentage = models.IntegerField(default=40)
    num_results = models.IntegerField(default=30)

    def save(self, *args, **kwargs):
        """Ensure only one instance of RecommendationSettings exists (singleton pattern)."""
        if not self.pk and RecommendationSettings.objects.exists():
            raise ValidationError("Only one RecommendationSettings instance is allowed.")
        return super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Retrieve or create the singleton instance of RecommendationSettings."""
        instance, _ = cls.objects.get_or_create(id=1)
        return instance

    def __str__(self):
        """Return string representation of the model."""
        return "Recommendation Settings"

    class Meta:
        """Meta options for RecommendationSettings model."""

        verbose_name = "Recommendation Setting"
        verbose_name_plural = "Recommendation Settings"
