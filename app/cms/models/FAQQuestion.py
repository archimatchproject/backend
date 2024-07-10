"""
Module defining the FAQQuestion model.

This module contains the FAQQuestion class, which represents
a frequently asked question related to a specific thematic in the application.
"""

from django.db import models

from app.cms.models.FAQThematic import FAQThematic
from app.core.models.BaseModel import BaseModel


class FAQQuestion(BaseModel):
    """
    Model representing a frequently asked question.

    Attributes:
        question (str): The text of the question.
        response (str): The text of the response.
        faq_thematic (ForeignKey): The thematic this question belongs to.
    """

    question = models.CharField(max_length=255)
    response = models.TextField()
    faq_thematic = models.ForeignKey(
        FAQThematic, on_delete=models.CASCADE, related_name="faq_thematic_questions"
    )

    class Meta:
        """
        Meta class for FAQQuestion model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "FAQQuestion"
        verbose_name_plural = "FAQQuestions"
