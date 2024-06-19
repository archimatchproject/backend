from django.contrib.auth.models import Permission
from django.db import models

from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.utils.PermissionsCodeNames import permission_codenames
from app.utils.models import BaseModel


class Admin(BaseModel):
    """
    Model representing an administrative user with extended permissions.

    Attributes:
        super_user (BooleanField): Indicates if the user has superuser privileges.
        user (OneToOneField): Associated ArchimatchUser instance for this admin.
        permissions (ManyToManyField): Permissions granted to this admin.

    Methods:
        __str__(): Returns the email address of the associated user.
        set_permissions(rights): Assigns permissions based on a list of rights.
        has_permission(perm): Checks if the admin has a specific permission.
    """

    super_user = models.BooleanField(default=False)
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.user.email

    def set_permissions(self, rights):
        for right in rights:
            if right in permission_codenames:
                for codename in permission_codenames[right]:
                    perm = Permission.objects.get(codename=codename)
                    self.permissions.add(perm)

    def has_permission(self, perm):
        if self.super_user:
            return True
        return self.permissions.filter(codename=perm).exists()
