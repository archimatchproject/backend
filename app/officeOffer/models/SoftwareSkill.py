"""
Module defining the SoftwareSkill model.

This module contains the SoftwareSkill class, which represents
the software skills of an architect in the application.
"""

from django.db import models


class SoftwareSkill(models.Model):
    """
    Model representing software skills of architects.
    """

    # Champ pour le nom de la compétence logicielle
    label = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Meta class for SoftwareSkill model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Software Skill"
        verbose_name_plural = "Software Skills"

    def __str__(self):
        """
        Return a string representation of the software skill.

        Returns:
            str: String representation of the software skill, including its label.
        """
        return self.label
