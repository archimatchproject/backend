"""
Module defining the TechnicalSkill model.

This module contains the TechnicalSkill class, which represents
the technical skills of an architect in the application.
"""

from django.db import models


class TechnicalSkill(models.Model):
    """
    Model representing technical skills of architects.
    """

    # Champ pour le nom de la compétence technique
    label = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Meta class for TechnicalSkill model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Technical Skill"
        verbose_name_plural = "Technical Skills"

    def __str__(self):
        """
        Return a string representation of the technical skill.

        Returns:
            str: String representation of the technical skill, including its label.
        """
        return self.label
