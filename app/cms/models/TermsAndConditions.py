"""
Module defining the TermsAndConditions model.

This module contains the TermsAndConditions model, representing
the terms and conditions (CGU/CGV) content of the application, with a restriction
that only one instance of this model can exist.
"""

from django.db import models

from rest_framework.serializers import ValidationError

from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin


class TermsAndConditions(BaseModel):
    """
    Model representing the terms and conditions (CGU/CGV).

    This model stores the content of the terms and conditions and
    references the admin who created it. Only one instance
    of this model can exist in the database.
    """

    content = models.TextField()
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        Return the string representation of the TermsAndConditions instance.
        """
        return "Terms and Conditions"

    def save(self, *args, **kwargs):
        """
        Override save method to enforce singleton behavior.
        """
        if not self.pk and TermsAndConditions.objects.exists():
            raise ValidationError(detail="Only one instance of TermsAndConditions is allowed.")
        return super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for TermsAndConditions model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Terms and Conditions"
        verbose_name_plural = "Terms and Conditions"
