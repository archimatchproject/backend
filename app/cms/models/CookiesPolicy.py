"""
Module defining the CookiesPolicy model.

This module contains the CookiesPolicy model, representing
the cookies policy content of the application, with a restriction
that only one instance of this model can exist.
"""

from django.db import models

from rest_framework.serializers import ValidationError

from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin


class CookiesPolicy(BaseModel):
    """
    Model representing the cookies policy.

    This model stores the content of the cookies policy and
    references the admin who created it. Only one instance
    of this model can exist in the database.
    """

    content = models.TextField()
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        Return the string representation of the CookiesPolicy instance.
        """
        return "Cookies Policy"

    def save(self, *args, **kwargs):
        """
        Override save method to enforce singleton behavior.
        """
        if not self.pk and CookiesPolicy.objects.exists():
            raise ValidationError(detail="Only one instance of CookiesPolicy is allowed.")
        return super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for CookiesPolicy model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Cookies Policy"
        verbose_name_plural = "Cookies Policies"
