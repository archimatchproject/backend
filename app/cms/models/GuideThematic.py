"""
Module defining the GuideThematic model.

This module contains the GuideThematic class, which represents
a thematic category for guide articles in the application.
"""

from django.db import models

from app.core.models.LabeledIcon import LabeledIcon


class GuideThematic(LabeledIcon):
    """
    Model representing a thematic category for guide articles.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    Attributes:
        icon (ImageField): Icon image associated with the guide thematic.
    """

    icon = models.ImageField(upload_to="icons/GuideThematicIcons/", blank=True, null=True)

    class Meta:
        """
        Meta class for GuideThematic model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "GuideThematic"
        verbose_name_plural = "GuideThematics"
