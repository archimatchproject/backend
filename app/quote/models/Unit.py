"""
Unit model representing a unit of measurement.
Attributes:
    title (CharField): The name of the unit, which must be unique and have a maximum length of 100 characters.
Meta:
    verbose_name (str): The human-readable name for the model, used in the Django admin interface.
    verbose_name_plural (str): The plural form of the human-readable name for the model, used in the Django
    admin interface.
Methods:
    __str__(): Returns the title of the Unit instance as its string representation.

"""

from django.db import models

from app.core.models.BaseModel import BaseModel


class Unit(BaseModel):
    """
    Unit model representing a measurement unit.
    Attributes:
        title (str): The name of the unit, which must be unique and is limited to 100 characters.
    Meta:
        verbose_name (str): The human-readable name for the model in singular form.
        verbose_name_plural (str): The human-readable name for the model in plural form.
    Methods:
        __str__(): Returns the title of the Unit instance as its string representation.
    """

    title = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Meta options for Unit model.

        The title field is unique, ensuring that no two units have the same name.
        This ensures that unit names such as 'kg' or 'liters' are unique across
        the system. The verbose name options control how this model is presented
        in the Django admin interface.
        """

        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        """
        Returns a string representation of the Unit instance.
        Returns:
            str: The title of the Unit.
        """

        return self.title
