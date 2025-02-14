from app.recommendation.models.ArchitectBox import ArchitectBox
from django.db import IntegrityError


def handle_architect_box_assignment(announcement, architects_results):
    """
    Assign announcements to architects' boxes based on results.

    Args:
        announcement (Announcement): The announcement instance.
        architects_results (list): List of architects returned by score computation.
    """
    if len(architects_results) < 10:
        print("Not enough results")

    for architect_data in architects_results:
        architect_id = architect_data.get("id")
        print(f"Processing Architect {architect_id}")
        try:
            architect_box, created = ArchitectBox.objects.get_or_create(
                architect_id=architect_id
            )

            if architect_box.announcements.count() < 8:
                architect_box.announcements.add(announcement)
                architect_box.save()
                print(
                    f"Added announcement {announcement.id} to ArchitectBox {architect_box.id}"
                )
            else:
                print(
                    f"ArchitectBox for Architect {architect_id} has reached maximum announcements"
                )
        except IntegrityError:
            print(f"Architect {architect_id} does not exist. Skipping.")
