"""
signals for users app
"""

from django.db.models.signals import post_delete
from django.dispatch import receiver

from app.users.models.Admin import Admin
from app.users.models.Architect import Architect
from app.users.models.Client import Client
from app.users.models.Supplier import Supplier


@receiver(post_delete, sender=Admin)
@receiver(post_delete, sender=Architect)
@receiver(post_delete, sender=Client)
@receiver(post_delete, sender=Supplier)
def delete_associated_user(sender, instance, **kwargs):
    """
    Deletes the associated ArchimatchUser when the user type instance is deleted.
    """
    if instance.user:
        instance.user.delete()
