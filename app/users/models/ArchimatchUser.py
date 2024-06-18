from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from app.users.models.utils.UserType import USER_TYPE_CHOICES


class ArchimatchUser(AbstractUser):
    image = models.ImageField(blank=True, null=True, upload_to="ProfileImages/")
    phone_number = models.CharField(max_length=20, unique=True, null=True)
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
