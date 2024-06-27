"""
Module containing the ArchimatchUser model.

This module defines the custom user model for the Archimatch application, extending the AbstractUser model.

Classes:
    ArchimatchUser: Custom user model for the Archimatch application.
"""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from app.users import USER_TYPE_CHOICES


class ArchimatchUser(AbstractUser):
    """
    Custom user model for the Archimatch application.

    Attributes:
        image (ImageField): Optional profile image for the user. Stored in 'ProfileImages/' directory.
        phone_number (CharField): Unique phone number of the user, maximum length of 20 characters.
        user_type (CharField): Type of the user, selected from choices defined in USER_TYPE_CHOICES.
        groups (ManyToManyField): Groups to which the user belongs.
        user_permissions (ManyToManyField): Permissions assigned to the user.

    """

    image = models.ImageField(blank=True, null=True, upload_to="ProfileImages/")
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    user_type = models.CharField(
        max_length=200, choices=USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0][0]
    )

    groups = models.ManyToManyField(
        Group, related_name="groups_archimatchuser_set", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="user_permissions_archimatchuser_set", blank=True
    )

    def __str__(self):
        """
        Returns the email address of the user as a string representation.

        Returns:
            str: The email address of the user.
        """
        return self.email

    def get_user_type(self):
        """
        Returns the user type of the user.

        Returns:
            str: The user type.
        """
        return self.user_type

    def save(self, *args, **kwargs):
        """
        Custom save method to set the username to email if not provided.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for ArchimatchUser model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Archimatch User"
