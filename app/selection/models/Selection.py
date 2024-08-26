from django.db import models
from app.selection import INTERESTED
from app.selection import SELECTION_STATUS_CHOICES

class Selection(models.Model):
    """
    Model representing the selection of architects for an announcement.

    Attributes:
        announcement (ForeignKey): The announcement that the architect is interested in.
        architect (ForeignKey): The architect who is interested in the announcement.
        status (CharField): The status of the selection (e.g., 'Interested', 'Accepted', 'Rejected').
    """


    announcement = models.ForeignKey("announcement.Announcement", on_delete=models.CASCADE, related_name='selections')
    architect = models.ForeignKey("users.Architect", on_delete=models.CASCADE, related_name='selections')
    status = models.CharField(max_length=10, choices=SELECTION_STATUS_CHOICES, default=INTERESTED)

    class Meta:
        unique_together = ('announcement', 'architect')
        constraints = [
            models.UniqueConstraint(
                fields=['announcement'],
                condition=models.Q(status='accepted'),
                name='unique_accepted_architect_per_announcement'
            ),
        ]
        verbose_name = "Selection"
        verbose_name_plural = "Selections"

    def __str__(self):
        return f"{self.architect} for {self.announcement}"
