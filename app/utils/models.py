"""
Module-level Doc for BaseModel
"""
from django.db import models
from django.utils import timezone

from app.cms.models import *
from app.users.models import *


class BaseModel(models.Model):
    """
    Define a base model with common fields for tracking creation and update timestamps.
    """

    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class to specify that this model is abstract."""

        abstract = True
