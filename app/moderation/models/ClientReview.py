"""
Module for the ClientReview model.

This module defines the ClientReview model, which represents the reviews
submitted by clients for architects.
"""

from django.db import models

from rest_framework.serializers import ValidationError

from app.core.models.BaseModel import BaseModel
from app.users.models.Architect import Architect
from app.users.models.Client import Client


class ClientReview(BaseModel):
    """
    Model representing a review submitted by a client for an architect.

    Attributes:
        architect (ForeignKey): The architect being reviewed.
        client (ForeignKey): The client who wrote the review.
        rating (FloatField): Numerical rating for the architect.
        comment (TextField): The review text.
    """

    architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField()

    def clean(self):
        """
        Custom validation for rating field to ensure it is between 0 and 5.
        """
        if not (0 <= self.rating <= 5):
            raise ValidationError("Rating must be between 0 and 5.")

    def __str__(self):
        """
        String representation of the ClientReview model.

        Returns:
            str: A string indicating the client and architect involved in the review.
        """
        return f"Review by {self.client} for {self.architect}"

    class Meta:
        """
        Meta class for ClientReview model.

        Meta Attributes:
            unique_together (tuple): Ensures that a client can submit only one review per architect.
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        unique_together = ("architect", "client")
        verbose_name = "Client Review"
        verbose_name_plural = "Client Reviews"
