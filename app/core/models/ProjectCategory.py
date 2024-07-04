"""
Module defining the ProjectCategory model.

This module contains the ProjectCategory class, which represents a category of project
in the application, inheriting from the LabeledIcon base class.
"""

from django.db import models

from app.core.models import LabeledIcon


class ProjectCategory(LabeledIcon):
    """
    Model representing a category of project, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.
    """

    icon = models.ImageField(upload_to="ProjectCategoryIcons/")

    class Meta:
        """
        Meta class for Project Category model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
