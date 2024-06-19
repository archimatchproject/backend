from django.db import models

from app.announcement.models.LabeledIcon import LabeledIcon


class ProjectCategory(LabeledIcon):
    """
    Model representing a category of project, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    This class inherits all fields and behavior from LabeledIcon.
    """

    pass

    class Meta:
        """Meta class for Project Category model."""

        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
