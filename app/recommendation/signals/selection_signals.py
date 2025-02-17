from django.db.models.signals import post_save
from django.dispatch import receiver
from app.selection.models.Selection import Selection
from app.recommendation.models.ArchitectBox import ArchitectBox
from app.recommendation.documents.ArchitectDocument import ArchitectDocument

@receiver(post_save, sender=Selection)
def handle_selection_created(sender, instance, created, **kwargs):
    """
    1. Remove the announcement from the selecting architect's box when a selection is made.
    2. If the number of selections for this announcement reaches 4, remove it from all architect boxes.
    3. Update the architect's document in Elasticsearch.
    """
    #1
    if created:
        architect_box = ArchitectBox.objects.get(architect_id=instance.architect.id)
        if instance.announcement in architect_box.announcements.all():
            architect_box.announcements.remove(instance.announcement)
            architect_box.save()
    #2
    selection_count = Selection.objects.filter(announcement=instance.announcement).count()
    if selection_count == 4:
    
        architect_boxes = ArchitectBox.objects.filter(announcements=instance.announcement)
        for box in architect_boxes:
            box.announcements.remove(instance.announcement)
            box.save()
    #3      
    ArchitectDocument().update(instance.architect)