"""
Module defining the ProjectExtension model.

This module contains the ProjectExtension classe,
representing different aspects of a project in the application.
"""

from django.core.exceptions import ValidationError
from django.db import models

from app.announcement.models.ProjectCategory import ProjectCategory
from app.core.models import LabeledIcon


class ProjectExtension(LabeledIcon):
    """
    Model representing an extension or additional feature for a project, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.
    """

    pass

    class Meta:
        """
        Meta class for Project Extension model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Project Extension"
        verbose_name_plural = "Project Extensions"
