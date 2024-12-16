"""
This module defines the ActionLog model, which is used to track administrative actions 
performed on projects, such as changing deadlines, canceling, blocking, or rebroadcasting projects.
"""


from django.db import models
from app.selection import ACTION_CHOICES
from app.users.models import Admin




class ActionLog(models.Model):
    """
    ActionLog model is used to store logs of actions performed by admin users 
    on different projects. It tracks the user, the type of action, the time of the action, 
    and optional additional details related to the action.
    """

    admin = models.ForeignKey(
        Admin, on_delete=models.CASCADE, related_name="action_logs",
        help_text="The admin user who performed the action."
    )
    action = models.CharField(
        max_length=50, choices=ACTION_CHOICES,
        help_text="The type of action performed (e.g., Change deadline, Cancel project)."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="The time when the action was performed."
    )
    details = models.JSONField(
        blank=True, null=True,
        help_text="Optional additional details about the action."
    )

    def __str__(self):
        """
        Returns a string representation of the ActionLog instance.
        
        :return: A string in the format '<username> - <action> - <timestamp>'.
        """
        return f"{self.admin.user.first_name} - {self.action} - {self.timestamp}"
