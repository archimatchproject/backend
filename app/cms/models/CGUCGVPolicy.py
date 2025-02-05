"""
Module defining the CGUCGVPolicy model.

This module contains the CGUCGVPolicy model, representing
the CGU (Conditions Générales d'Utilisation) and CGV (Conditions Générales de Vente)
content of the application, with a restriction that only one instance of this model can exist.
"""

from django.db import models
from rest_framework.serializers import ValidationError
from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin


class CGUCGVPolicy(BaseModel):
    """
    Model representing the CGU and CGV policy content.

    This model stores the combined content of both the CGU (Terms of Use) 
    and CGV (Terms of Sale) and references the admin who created it.
    Only one instance of this model can exist in the database.
    """

    content = models.TextField("CGU/CGV Content")
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        Return the string representation of the CGUCGVPolicy instance.
        """
        return "CGU/CGV Policy"

    def save(self, *args, **kwargs):
        """
        Override save method to enforce singleton behavior.
        """
        if not self.pk and CGUCGVPolicy.objects.exists():
            raise ValidationError(detail="Only one instance of CGU/CGV Policy is allowed.")
        return super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for CGUCGVPolicy model.
        """
        verbose_name = "CGU/CGV Policy"
        verbose_name_plural = "CGU/CGV Policies"
