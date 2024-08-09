"""
Module defining the PrivacyPolicy model.

This module contains the PrivacyPolicy model, representing
the privacy policy content of the application, with a restriction
that only one instance of this model can exist.
"""

from django.db import models

from rest_framework.serializers import ValidationError

from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin


class PrivacyPolicy(BaseModel):
    """
    Model representing the privacy policy.

    This model stores the content of the privacy policy and
    references the admin who created it. Only one instance
    of this model can exist in the database.
    """

    content = models.TextField()
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        Return the string representation of the PrivacyPolicy instance.
        """
        return "Privacy Policy"

    def save(self, *args, **kwargs):
        """
        Override save method to enforce singleton behavior.
        """
        if not self.pk and PrivacyPolicy.objects.exists():
            raise ValidationError(detail="Only one instance of PrivacyPolicy is allowed.")
        return super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for PrivacyPolicy model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policies"
