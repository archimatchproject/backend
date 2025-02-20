"""
This module defines the AnnouncementWeights model, which represents weights for various
announcement attributes.The weights are used to calculate the relevance of announcements
based on different criteria.

Classes:
    AnnouncementWeights: A Django model representing the weights for various announcement
    attributes.
"""

from django.db import models


class AnnouncementWeights(models.Model):
    """
    Model representing weights for various announcement attributes.

    Attributes:
        architectural_style (int): Weight for architectural style matching.
        work_type (int): Weight for work type matching.
        project_category (int): Weight for project category matching.
        property_types (int): Weight for property type matching.
        needs_per_match (int): Weight for needs per match criteria.
    """

    architectural_style = models.IntegerField(default=10)
    work_type = models.IntegerField(default=8)
    project_category = models.IntegerField(default=6)
    property_type = models.IntegerField(default=5)
    needs_per_match = models.IntegerField(default=2)

    def __str__(self):
        """Return string representation of the model."""
        return "Announcement Weights"
