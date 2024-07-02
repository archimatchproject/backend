from django.contrib.auth.models import Permission
from django.db import models

from app.core.models import BaseModel
from app.users import PERMISSION_CODENAMES
from app.users.models.ArchimatchUser import ArchimatchUser


class Admin(BaseModel):
    """
    Model representing an administrative user with extended permissions.

    Attributes:
        super_user (BooleanField): Indicates if the user has superuser privileges.
        user (OneToOneField): Associated ArchimatchUser instance for this admin.
        permissions (ManyToManyField): Permissions granted to this admin.
    """

    super_user = models.BooleanField(default=False)
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        """
        Returns the email address of the associated user.

        Returns:
            str: The email address of the user.
        """
        return self.user.email

    @property
    def permissions_list(self):
        """
        Returns a list of codenames of permissions granted to this admin.
        """
        return list(self.permissions.values_list('codename', flat=True))

    @property
    def is_supper_user(self):
        """
        Checks if the admin has superuser privileges.
        """
        return self.super_user

    def set_permissions(self, rights):
        """
        Assigns permissions based on a list of rights.

        Args:
            rights (list): List of rights to assign permissions for.
        """
        for right in rights:
            if right in PERMISSION_CODENAMES:
                for codename in PERMISSION_CODENAMES[right]:
                    perm = Permission.objects.get(codename=codename)
                    self.permissions.add(perm)

    def has_permission(self, perm):
        """
        Checks if the admin has a specific permission.

        Args:
            perm (str): The codename of the permission to check.

        Returns:
            bool: True if the admin has the permission, False otherwise.
        """
        if self.super_user:
            return True
        return self.permissions.filter(codename=perm).exists()

    class Meta:
        """
        Meta class for Admin model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Admin"
        verbose_name_plural = "Admins"
