"""
Module containing the ArchimatchUser model.

This module defines the custom user model for the Archimatch application, extending the
AbstractUser model.

Classes:
    ArchimatchUser: Custom user model for the Archimatch application.
"""

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.users import USER_TYPE_CHOICES


class ArchimatchUser(AbstractUser):
    """
    Custom user model for the Archimatch application.

    Attributes:
        image (ImageField): Optional profile image for the user. Stored in
         'ProfileImages/' directory.
        phone_number (CharField): Unique phone number of the user, maximum
         length of 20 characters.
        user_type (CharField): Type of the user, selected from choices defined
         in USER_TYPE_CHOICES.
        groups (ManyToManyField): Groups to which the user belongs.
        user_permissions (ManyToManyField): Permissions assigned to the user.

    """

    email = models.EmailField(
        _("email address"),
        blank=True,
        unique=True,
    )
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="ProfileImages/",
    )
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    user_type = models.CharField(
        max_length=200,
        choices=USER_TYPE_CHOICES,
        default=USER_TYPE_CHOICES[0][0],
    )

    groups = models.ManyToManyField(
        Group,
        related_name="groups_archimatchuser_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permissions_archimatchuser_set",
        blank=True,
    )
    is_deleted = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    suspension_start_date = models.DateField(null=True, blank=True)
    suspension_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        Returns the email address of the user as a string representation.

        Returns:
            str: The email address of the user.
        """
        return self.email

    @property
    def user_type_display(self):
        """
        Returns the display name of the user type.
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
        verbose_name_plural = "Archimatch Users"
