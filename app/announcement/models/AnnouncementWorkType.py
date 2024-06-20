"""
Module defining the AnnouncementWorkType model.

This module contains the AnnouncementWorkType class, which represents
work types for announcements in the Archimatch application.
"""

from django.db import models


class AnnouncementWorkType(models.Model):
    """
    Model representing work types for announcements in the Archimatch application.

    Attributes:
        header (CharField): Header or title of the work type, maximum length of 255 characters.
        description (CharField): Description of the work type, maximum length of 255 characters.
    """

    header = models.CharField(max_length=255, default="")
    description = models.CharField(max_length=255, default="")

    def __str__(self) -> str:
        """
        String representation of the AnnouncementWorkType instance.

        Returns:
            str: Header or title of the work type.
        """
        return self.header

    class Meta:
        """
        Meta class for Announcement Work Type model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Announcement Work Type"
        verbose_name_plural = "Announcement Work Types"
