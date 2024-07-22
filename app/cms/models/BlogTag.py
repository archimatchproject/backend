"""
Module defining the BlogTag model.

This module contains the BlogTag class, which represents a tag for categorizing blog posts.
"""

from django.db import models


class BlogTag(models.Model):
    """
    Model representing a tag for categorizing blog posts.

    Attributes:
        name (str): The name of the tag.
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        """
        Meta class for BlogTag model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"

    def __str__(self):
        """
        String representation of the blog tag.
        """
        return self.name
