"""
Module containing the WorkSurface model.

This module defines the WorkSurface model, representing the possible work surfaces
associated with an architect within the Archimatch application.

Classes:
    WorkSurface: Define the WorkSurface model with a name field and choices.
"""

from django.db import models

from app.announcement import WORK_SURFACES


class WorkSurface(models.Model):
    """
    Define the WorkSurface model.

    Fields:
        name (CharField): The name of the work surface, chosen from a predefined list.
    """

    name = models.CharField(max_length=50, choices=WORK_SURFACES)

    def __str__(self):
        """
        Returns the name of the work surface.

        Returns:
            str: The name of the work surface.
        """
        return self.name
