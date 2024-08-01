"""
Module containing the PreferredLocation model.

This module defines the PreferredLocation model,
representing the locations that an architect prefers
to work in within the Archimatch application.

Classes:
    PreferredLocation: Define the PreferredLocation model with a name field.
"""

from django.db import models


class PreferredLocation(models.Model):
    """
    Define the PreferredLocation model.

    Fields:
        name (CharField): The name of the preferred location.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns the name of the preferred location.

        Returns:
            str: The name of the preferred location.
        """
        return self.name
