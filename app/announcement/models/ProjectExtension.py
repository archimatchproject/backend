"""
Module defining the ProjectExtension model.

This module contains the ProjectExtension classe,
representing different aspects of a project in the application.
"""

from django.db import models

from app.core.models import LabeledIcon
from app.core.models.PropertyType import PropertyType


class ProjectExtension(LabeledIcon):
    """
    Model representing an extension or additional feature for a project, inheriting from
    LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.
    """

    icon = models.ImageField(upload_to="ProjectExtensionIcons/")
    property_type = models.ForeignKey(
        PropertyType,
        related_name="property_type_project_extensions",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        """
        Meta class for Project Extension model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Project Extension"
        verbose_name_plural = "Project Extensions"
