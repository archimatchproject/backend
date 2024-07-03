"""
Module for defining preference models dynamically based on CHOICE_MODEL_NAMES.
"""

from django.db import models


class Preference(models.Model):
    """
    Abstract base model for preferences.
    """

    name = models.CharField(max_length=255)

    class Meta:
        """
        Meta class for Architect Preference models.


        """

        abstract = True

    def __str__(self):
        """
        String representation of the preference object.
        """
        return self.name


# Define choice model names
CHOICE_MODEL_NAMES = [
    "WorkType",
    "HouseType",
    "ServiceType",
    "LocationType",
    "WorkSurfaceType",
    "BudgetType",
]

# Dynamically create choice models inheriting from Preference
for model_name in CHOICE_MODEL_NAMES:
    # Dynamically create the model class
    globals()[model_name] = type(
        model_name,
        (Preference,),
        {"__module__": __name__},
    )
