"""
This module provides utility functions for handling architect box assignments.
Functions:
    handle_architect_box_assignment(announcement, architects_results):
        Assigns announcements to architects' boxes based on the provided results.

"""

from django.db import IntegrityError

from app.recommendation.models.ArchitectBox import ArchitectBox


def handle_architect_box_assignment(announcement, architects_results):
    """
    Assign announcements to architects' boxes based on results.

    Args:
        announcement (Announcement): The announcement instance.
        architects_results (list): List of architects returned by score computation.
    """
    if len(architects_results) < 10:
        pass

    for architect_data in architects_results:
        architect_id = architect_data.get("id")

        try:
            architect_box, created = ArchitectBox.objects.get_or_create(architect_id=architect_id)

            if architect_box.announcements.count() < 8:
                architect_box.announcements.add(announcement)
                architect_box.save()
        except IntegrityError:
            pass
