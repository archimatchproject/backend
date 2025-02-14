from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.users.models.Architect import Architect
from app.recommendation.documents.ArchitectDocument import ArchitectDocument
from app.announcement.models.Announcement import Announcement
from app.recommendation.services.recommend_architects import compute_architect_score
from app.recommendation.utils import handle_architect_box_assignment
from app.selection.models.Selection import Selection
from app.recommendation.models.ArchitectBox import ArchitectBox


# Sync Elasticsearch when an Announcement is saved
@receiver(post_save, sender=Architect)
def index_architect(sender, instance, **kwargs):
    ArchitectDocument().update(instance)


# Remove from Elasticsearch when an Announcement is deleted
@receiver(post_delete, sender=Architect)
def delete_architect(sender, instance, **kwargs):
    ArchitectDocument().delete(instance)


@receiver(post_save, sender=Announcement)
def handle_announcement_creation(sender, instance, created, **kwargs):
    """
    Run this function only when a new Announcement is created.

    Args:
        sender: The model class that triggered the signal.
        instance: The actual instance being saved.
        created: Boolean; True if a new record was created.
        kwargs: Additional keyword arguments.
    """
    if created:
        # Perform desired actions here when a new announcement is created
        architects_results = compute_architect_score(
            projet=instance,
            attributes=[
                "architectural_style",
                "work_type",
                "project_category",
                "property_type",
            ],
            many_to_many_fields=["needs"],
            weights={
                "distance": 25,
                "perfect_match": 5,
                "architectural_style": 10,
                "work_type": 8,
                "project_category": 6,
                "needs_per_match": 2,
                "on_going_projects": 5,
                "property_types": 5,
            },
            distance_limit=200,
            score_percentage=40,
            num_results=30,
            attribute_mapping={
                "architectural_style": "architectural_styles",
                "work_type": "work_types",
                "project_category": "project_categories",
                "needs": "needs",
                "property_type": "property_types",
            },
        )
        print(f"Announcement {instance.id} created. Result: {architects_results}")
        print(f"Architect search returned {len(architects_results)} results")
        handle_architect_box_assignment(instance, architects_results)


@receiver(post_save, sender=Selection)
def handle_selection_created(sender, instance, created, **kwargs):
    """Remove announcement from architect's box when a selection is made."""
    if created:
        architect_box = ArchitectBox.objects.get(architect_id=instance.architect.id)
        if instance.announcement in architect_box.announcements.all():
            architect_box.announcements.remove(instance.announcement)
            architect_box.save()
