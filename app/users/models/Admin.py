from django.db import models
from app.users.models.ArchimatchUser import ArchimatchUser
from django.contrib.auth.models import Permission
from app.users.models.utils.PermissionsCodeNames import permission_codenames
from app.models import BaseModel


class Admin(BaseModel):

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
