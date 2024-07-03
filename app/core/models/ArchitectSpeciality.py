"""
Module defining the ArchitectSpeciality model.

This module contains the ArchitectSpeciality class, which represents
the specialty of an architect in the application.
"""

from django.db import models


class ArchitectSpeciality(models.Model):
    """
    Model representing the specialty of an architect.

    label
    icon
    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="ArchitectSpecialityIcons/")

    def __str__(self):
        """
        Return a string representation of the labeled icon.

        Returns:
            str: Label or name associated with the icon.
        """
        return self.label

    class Meta:
        """
        Meta class for Architect Speciality model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Architect Speciality"
        verbose_name_plural = "Architect Specialities"
