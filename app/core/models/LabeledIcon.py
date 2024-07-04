"""
Module defining the LabeledIcon model.

This module contains the LabeledIcon class, which represents a labeled icon
with a label and an associated image in the application.
"""

from django.db import models


class LabeledIcon(models.Model):
    """
    Model representing a labeled icon with a label and an associated image.

    Attributes:
        label (CharField): Label or name associated with the icon, maximum length of 255 characters.
        icon (ImageField): Image file representing the icon, stored in 'Icons/' directory.
    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="LabeledIcons/")

    def __str__(self):
        """
        Return a string representation of the labeled icon.

        Returns:
            str: Label or name associated with the icon.
        """
        return self.label

    class Meta:
        """
        Meta class for Labeled Icon model.

        Provides verbose names for the model in the Django admin interface.
        """

        abstract = True
        verbose_name = "Labeled Icon"
        verbose_name_plural = "Labeled Icons"
