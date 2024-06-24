"""
Module defining the AnnouncementPieceRenovate model.

This module contains the AnnouncementPieceRenovate class, which represents an AnnouncementPieceRenovate
for a construction or renovation project in the application.
"""
from django.db import models

from app.announcement.models.Announcement import Announcement
from app.announcement.models.PieceRenovate import PieceRenovate


class AnnouncementPieceRenovate(models.Model):
    """
    Model representing the relationship between Announcement and PieceRenovate
    with an additional field for the number of each piece to be renovated.
    """

    announcement = models.ForeignKey(
        Announcement, on_delete=models.CASCADE, related_name="pieces_renovate"
    )
    piece_renovate = models.ForeignKey(PieceRenovate, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(default=0)

    class Meta:
        """
        Meta class for AnnouncementPieceRenovate model.

        Provides unique constraint to prevent duplicate entries.
        """

        unique_together = ("announcement", "piece_renovate")

    def __str__(self):
        """
        Return a string representation of the annoucement piece renovate.

        Returns:
            str: String representation of the annoucement piece renovate, including its ID and associated client.
        """
        return f"{self.announcement} - {self.piece_renovate} ({self.number})"
