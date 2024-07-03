"""
Module defining the ProjectCategory model.

This module contains the ProjectCategory class, which represents a category of project
in the application.
"""

from django.db import models


class ProjectCategory(models.Model):
    """
    Model representing a category of project.

    label
    icon
    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="ProjectCategoryIcons/")

    def __str__(self):
        """
        Return a string representation of the labeled icon.

        Returns:
            str: Label or name associated with the icon.
        """
        return self.label

    class Meta:
        """
        Meta class for Project Category model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
