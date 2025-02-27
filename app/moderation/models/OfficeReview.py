"""
This module defines the OfficeReview model, which allows offices to review architects.

The OfficeReview model stores ratings and comments submitted by offices for architects.
Each review is unique per office-architect pair, ensuring that an office cannot review
the same architect multiple times. The model also includes validation to restrict
ratings to predefined values (1, 2, or 3).
"""

from django.core.exceptions import ValidationError
from django.db import models

from app.core.models import BaseModel
from app.users.models import Architect
from app.users.models.Office import Office


class OfficeReview(BaseModel):
    """
    Model representing a review submitted by an office for an architect.

    Attributes:
        architect (ForeignKey): The architect being reviewed.
        office (ForeignKey): The office that submitted the review.
        rating (IntegerField): Rating given by the office (1, 2, or 3).
        comment (TextField): The review text.
    """

    architect = models.ForeignKey(Architect, on_delete=models.CASCADE, related_name="office_reviews")
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(1, "Poor"), (2, "Average"), (3, "Good")])
    comment = models.TextField()

    class Meta:
        """Meta options for OfficeReview model."""

        unique_together = ("architect", "office")

    def clean(self):
        """Ensure the rating is within the allowed range (1, 2, or 3)."""
        if self.rating not in [1, 2, 3]:
            raise ValidationError("Rating must be 1, 2, or 3.")

    def __str__(self):
        """
        Return a string representation of the review.

        Returns:
            str: A formatted string with the office name and architect.
        """
        return f"Review by {self.office.office_name} for {self.architect}"
