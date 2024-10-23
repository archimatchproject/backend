from django.db import models
from app.selection import INTERESTED
from app.selection import SELECTION_STATUS_CHOICES

from django.db import models
from django.utils.translation import gettext_lazy as _



class Selection(models.Model):
    """
    Model representing the selection of architects for an announcement.
    """

    announcement = models.ForeignKey(
        "announcement.Announcement",
        on_delete=models.CASCADE,
        related_name='selections'
    )
    architect = models.ForeignKey(
        "users.Architect",
        on_delete=models.CASCADE,
        related_name='selections'
    )
    status = models.CharField(
        max_length=10,
        choices=SELECTION_STATUS_CHOICES,
        default=INTERESTED
    )
    # One-to-one relationship with Phase
    phase = models.OneToOneField(
        'Phase',
        on_delete=models.CASCADE,
        related_name='selection',
        null=True,  
        blank=True  
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Selection Name")
    )
    
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
