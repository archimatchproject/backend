"""
Module defining the PropertyType model.

This module contains the PropertyType classe,
representing different aspects of a project in the application.
"""

from django.db import models

from app.core.models.ProjectCategory import ProjectCategory


class PropertyType(models.Model):
    """
    Model representing a type of property.



    Attributes:
        project_category (ForeignKey): Category of project associated with this property type.
        label
        icon
    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="PropertyTypeIcons/")

    def __str__(self):
        """
        Return a string representation of the labeled icon.

        Returns:
            str: Label or name associated with the icon.
        """
        return self.label

    project_category = models.ForeignKey(
        ProjectCategory,
        related_name="project_category_property_types",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        """
        Meta class for Property Type model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Property Type"
        verbose_name_plural = "Property Types"
