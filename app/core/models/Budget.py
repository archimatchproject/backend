"""
Module containing the Budget model.

This module defines the Budget model, representing the possible budget ranges
associated with an architect within the Archimatch application.

Classes:
    Budget: Define the Budget model with a name field and choices.
"""

from django.db import models

from app.announcement import BUDGETS


class Budget(models.Model):
    """
    Define the Budget model.

    Fields:
        name (CharField): The name of the budget range, chosen from a predefined list.
    """

    name = models.CharField(max_length=50, choices=BUDGETS)

    def __str__(self):
        """
        Returns the name of the budget range.

        Returns:
            str: The name of the budget range.
        """
        return self.name
