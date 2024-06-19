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

    Methods:
        __str__(): Returns the email address of the user as a string representation.
        get_user_type(): Returns the user type of the user.
        save(*args, **kwargs): Custom save method to set the username to email if not provided.
    """

    image = models.ImageField(blank=True, null=True, upload_to="ProfileImages/")
    phone_number = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=200, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(
        Group, related_name="archimatchuser_set", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="archimatchuser_set", blank=True
    )

    def __str__(self):
        return self.email

    def get_user_type(self):
        return self.user_type

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Archimatch User"
        verbose_name_plural = "Archimatch Users"
