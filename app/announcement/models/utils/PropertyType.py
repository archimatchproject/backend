from django.db import models

from .LabeledIcon import LabeledIcon
from .ProjectCategory import ProjectCategory


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
        default=None,
    )
