"""
Module defining the WorkType model.

This module contains the WorkType class, which represents
work types for announcements in the Archimatch application.
"""

from django.db import models

from app.core.models.PropertyType import PropertyType


class WorkType(models.Model):
    """
    Model representing work types for announcements in the Archimatch application.

    Attributes:
        header (CharField): Header or title of the work type, maximum length of 255 characters.
        description (CharField): Description of the work type, maximum length of 255 characters.
    """

    header = models.CharField(max_length=255, default="")
    description = models.CharField(max_length=255, default="")
    property_type = models.ForeignKey(
        PropertyType,
        related_name="property_type_work_types",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self) -> str:
        """
        String representation of the WorkType instance.

        Returns:
            str: Header or title of the work type.
        """
        return self.header

    class Meta:
        """
        Meta class for  Work Type model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = " Work Type"
        verbose_name_plural = " Work Types"
