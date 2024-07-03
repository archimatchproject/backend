"""
Module defining the PropertyType model.

This module contains the PropertyType classe,
representing different aspects of a project in the application.
"""

from django.db import models

from app.announcement.models.ProjectCategory import ProjectCategory
from app.core.models import LabeledIcon


class PropertyType(LabeledIcon):
    """
    Model representing a type of property, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    Attributes:
        project_category (ForeignKey): Category of project associated with this property type.
    """

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
