"""
Module: Verification Code Model

This module defines the VerificationCode model, used for managing client account verification
in the Archimatch application.
Each client can have a single, active 4-digit verification code that expires after 5 minutes.
This model provides functionality
for generating, regenerating, and checking the expiration of verification codes.

Classes:
    VerificationCode: Model representing a 4-digit verification code for a client with an
    expiration time.

Functions:
    generate_code(): Generates a random 4-digit code.
    create_or_regenerate_code(client): Creates a new verification code for a client, replacing
    any existing one.
"""

import random

from datetime import timedelta

from django.db import models
from django.utils import timezone

from app.core.models import BaseModel


class VerificationCode(BaseModel):
    """
    Model to store a 4-digit verification code for a client with an expiration time.

    Attributes:
        user (ForeignKey): The user this verification code is associated with.
        code (CharField): The 4-digit verification code.
        created_at (DateTimeField): Timestamp when the code was created.
    """

    user = models.OneToOneField("ArchimatchUser", on_delete=models.CASCADE, related_name="verification_code")
    code = models.CharField(max_length=4)

    def is_expired(self):
        """Check if the code is expired (5 minutes)."""
        return timezone.now() > self.created_at + timedelta(minutes=5)

    @staticmethod
    def generate_code():
        """Generate a random 4-digit code."""
        return f"{random.randint(1000, 9999)}"

    @classmethod
    def create_or_regenerate_code(cls, user):
        """Create or regenerate a verification code for the given client."""
        # Delete any existing code for this client
        cls.objects.filter(user=user).delete()

        # Create a new code
        return cls.objects.create(user=user, code=cls.generate_code())

    def __str__(self):
        """
        Returns a string representation of the VerificationCode instance.
        The string includes the user's email and the verification code.
        Returns:
            str: A formatted string containing the user's email and the verification code.
        """

        return f"Verification Code for {self.user.email}: {self.code}"
