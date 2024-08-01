"""
Module defining the GuideThematic model.

This module contains the GuideThematic class, which represents
a thematic category for guide articles in the application.
"""

from django.db import models

from app.cms import TARGET_USER_TYPE
from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin


class GuideThematic(BaseModel):
    """
    Model representing a thematic category for guide articles.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    Attributes:
        icon (ImageField): Icon image associated with the guide thematic.
    """

    title = models.CharField(max_length=255, unique=True)
    sub_title = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="icons/GuideThematicIcons/", blank=True, null=True)
    admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING)
    visible = models.BooleanField(default=False)
    target_user_type = models.CharField(
        max_length=10, choices=TARGET_USER_TYPE, default=TARGET_USER_TYPE[0][0]
    )

    def __str__(self):
        """
        String representation of the GuideThematic.
        """
        return self.title

    class Meta:
        """
        Meta class for GuideThematic model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "GuideThematic"
        verbose_name_plural = "GuideThematics"
