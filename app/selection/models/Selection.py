"""
Attributes:
    announcement (ForeignKey): Reference to the related announcement.
    architect (ForeignKey): Reference to the selected architect.
    status (CharField): Status of the selection, with choices defined in SELECTION_STATUS_CHOICES.
    phase (OneToOneField): One-to-one relationship with the Phase model, can be null or blank.
    name (CharField): Name of the selection, can be null or blank.
    is_client_interested (BooleanField): Indicates if the client is interested, defaults to True.
    is_abandoned (BooleanField): Indicates if the selection is abandoned, defaults to False.
    is_blocked (BooleanField): Indicates if the selection is blocked, defaults to False.
Meta:
    unique_together: Ensures that each combination of announcement and architect is unique.
    constraints: Ensures that only one architect can be accepted per announcement.
    verbose_name: Human-readable name for the model.
    verbose_name_plural: Human-readable plural name for the model.
Methods:
    __str__: Returns a string representation of the selection.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.selection import INTERESTED
from app.selection import SELECTION_STATUS_CHOICES


class Selection(models.Model):
    """
    Model representing the selection of architects for an announcement.
    """

    announcement = models.ForeignKey(
        "announcement.Announcement", on_delete=models.CASCADE, related_name="selections"
    )
    architect = models.ForeignKey(
        "users.Architect", on_delete=models.CASCADE, related_name="selections"
    )
    status = models.CharField(max_length=10, choices=SELECTION_STATUS_CHOICES, default=INTERESTED)
    # One-to-one relationship with Phase
    phase = models.OneToOneField(
        "Phase",
        on_delete=models.CASCADE,
        related_name="selection",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Selection Name"))
    is_client_interested = models.BooleanField(default=True)
    is_abandoned = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        """
        Meta class for the Selection model.
        Attributes:
            unique_together (tuple): Ensures that the combination of 'announcement' and 'architect' is unique.
            constraints (list): A list of constraints for the model. Includes a unique constraint on the 'announcement'
            field when the 'status' is 'accepted', ensuring that there is only one accepted architect per
            announcement.
            verbose_name (str): The human-readable name for the model.
            verbose_name_plural (str): The human-readable plural name for the model.
        """

        unique_together = ("announcement", "architect")
        constraints = [
            models.UniqueConstraint(
                fields=["announcement"],
                condition=models.Q(status="accepted"),
                name="unique_accepted_architect_per_announcement",
            ),
        ]
        verbose_name = "Selection"
        verbose_name_plural = "Selections"

    def __str__(self):
        """
        Returns a string representation of the Selection instance.
        The string representation includes the architect and the announcement
        associated with the selection.
        Returns:
            str: A string in the format "{architect} for {announcement}".
        """

        return f"{self.architect} for {self.announcement}"
