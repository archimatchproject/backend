"""
Module defining the FAQThematic model.

This module contains the FAQThematic class, which represents
a thematic category for frequently asked questions in the application.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel


class FAQThematic(BaseModel):
    """
    Model representing a thematic category for frequently asked questions.

    Attributes:
        title (str): The title of the thematic category.
    """

    title = models.CharField(max_length=255, unique=True)

    class Meta:
        """
        Meta class for FAQThematic model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "FAQThematic"
        verbose_name_plural = "FAQThematics"
