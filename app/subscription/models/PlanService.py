"""
Module containing the Service model.
"""

from django.contrib.auth.models import Permission
from django.db import models

from app.core.models.BaseModel import BaseModel


class PlanService(BaseModel):
    """
    Model representing a service with a set of permissions.
    """

    description = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        """
        String representation of the Service instance.
        """
        return self.description

    class Meta:
        """
        Meta class for PlanSerice model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Plan Serice"
        verbose_name_plural = "Plan Serices"