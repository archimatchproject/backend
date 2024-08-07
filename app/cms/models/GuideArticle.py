"""
Module defining the GuideArticle model.

This module contains the GuideArticle class, which represents
an article providing guidance on a specific thematic in the application.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from app.cms.models.GuideThematic import GuideThematic
from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin


class GuideArticle(BaseModel):
    """
    Model representing an article providing guidance on a specific thematic.

    Attributes:
        title (str): The title of the guide article.
        description (str): A brief description of the guide article.
        guide_thematic (ForeignKey): The thematic this article belongs to.
        date (date): The publication date of the guide article.
        rating (float): The rating of the guide article, from 0 to 5.
    """

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    guide_thematic = models.ForeignKey(
        GuideThematic, on_delete=models.CASCADE, related_name="guide_thematic_articles"
    )
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    visible = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    rating = models.FloatField()

    def clean(self):
        """
        Custom validation for rating field to ensure it is between 0 and 5.
        """
        if not (0 <= self.rating <= 5):
            raise ValidationError("Rating must be between 0 and 5.")

    def __str__(self):
        """
        String representation of the GuideArticle.
        """
        return self.title

    class Meta:
        """
        Meta class for GuideArticle model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "GuideArticle"
        verbose_name_plural = "GuideArticles"
