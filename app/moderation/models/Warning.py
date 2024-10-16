"""
Module for the Warning model.

This module defines the Warning model
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin
from app.users.models.ArchimatchUser import ArchimatchUser


class Warning(BaseModel):
    """
    Model to store warnings issued to users or entities based on reports.
    """

    issued_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    issued_for = models.ForeignKey(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the Warning model.
        """
        return f"Warning for {self.issued_for.email} by {self.issued_by.user.email}"

    class Meta:
        """
        Meta class for Warning_ model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Warning"
        verbose_name_plural = "Warnings"
