"""
Module containing the TerrainSurface model.

This module defines the TerrainSurface model, representing the possible terrain surfaces
associated with an architect within the Archimatch application.

Classes:
    TerrainSurface: Define the TerrainSurface model with a name field and choices.
"""

from django.db import models

from app.announcement import TERRAIN_SURFACES


class TerrainSurface(models.Model):
    """
    Define the TerrainSurface model.

    Fields:
        name (CharField): The name of the terrain surface, chosen from a predefined list.
    """

    name = models.CharField(max_length=50, choices=TERRAIN_SURFACES)

    def __str__(self):
        """
        Returns the name of the terrain surface.

        Returns:
            str: The name of the terrain surface.
        """
        return self.name
