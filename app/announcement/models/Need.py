"""
Module defining the Need model.

This module contains the Need class, which represents a specific need or requirement
in the application base class.
"""

from django.db import models

from app.core.models.ArchitectSpeciality import ArchitectSpeciality


class Need(models.Model):
    """
    Model representing a specific need or requirement.



    Attributes:
        architect_speciality (ForeignKey): Specialization of the architect related to this need.
        label
        icon
    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="NeedIcons/")

    architect_speciality = models.ForeignKey(
        ArchitectSpeciality,
        related_name="architect_speciality_needs",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        """
        Return a string representation of the labeled icon.

        Returns:
            str: Label or name associated with the icon.
        """
        return self.label

    class Meta:
        """
        Meta class for Need model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Need"
        verbose_name_plural = "Needs"
