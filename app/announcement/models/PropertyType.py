from django.db import models

from app.announcement.models.LabeledIcon import LabeledIcon
from app.announcement.models.ProjectCategory import ProjectCategory


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
        related_name="property_types",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        """Meta class for Property Type model."""

        verbose_name = "Property Type"
        verbose_name_plural = "Property Types"
