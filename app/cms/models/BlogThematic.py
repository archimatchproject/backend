"""
Module defining the BlogThematic model.

This module contains the BlogThematic class, which represents
a thematic category for blog posts in the application.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin


class BlogThematic(BaseModel):
    """
    Model representing a thematic category for blog posts.

    Attributes:
        title (str): The title of the thematic category.
        admin (ForeignKey): The admin who added the thematic category.
        visible (bool): Whether the thematic category is visible.
        last_update (DateTimeField): The date and time of the last update.
    """

    title = models.CharField(max_length=255, unique=True)
    admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING)
    visible = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for BlogThematic model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Blog Thematic"
        verbose_name_plural = "Blog Thematics"

    def __str__(self):
        """
        String representation of the blog thematic.
        """
        return self.title
