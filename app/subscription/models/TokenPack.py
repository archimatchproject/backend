"""
Module containing the TokenPack model.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel


class TokenPack(BaseModel):
    """
    Model representing a pack of tokens.
    """

    pack_name = models.CharField(max_length=255)
    pack_price = models.DecimalField(max_digits=10, decimal_places=2)
    number_tokens = models.PositiveIntegerField()
    number_free_tokens = models.PositiveIntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the TokenPack instance.
        """
        return self.pack_name

    class Meta:
        """
        Meta class for TokenPack model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Token Pack"
        verbose_name_plural = "Token Packs"
