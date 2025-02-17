from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.users.models.Architect import Architect
from app.recommendation.documents.ArchitectDocument import ArchitectDocument


# Sync Elasticsearch when an Announcement is saved
@receiver(post_save, sender=Architect)
def index_architect(sender, instance, **kwargs):
    ArchitectDocument().update(instance)


# Remove from Elasticsearch when an Announcement is deleted
@receiver(post_delete, sender=Architect)
def delete_architect(sender, instance, **kwargs):
    ArchitectDocument().delete(instance)