"""
This module contains the AppConfig class for configuring the 'app.announcement' Django application.
"""

from django.apps import AppConfig






class SelectionConfig(AppConfig):
    """
    AppConfig for the 'app.selection' Django application.

    This AppConfig defines configuration for the 'app.selection' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.selection"
    
    def ready(self):
        # Schedule the task if not already scheduled
        from background_task.models import Task
        from datetime import datetime, timedelta

        import pytz
        from app.selection.tasks.selection_phase_tasks import process_email_triggers
        timezone = pytz.timezone('UTC')
        now = datetime.now(timezone)
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        if not Task.objects.filter(task_name='app.selection.tasks.selection_phase_tasks.process_email_triggers').exists():
            process_email_triggers(repeat=24 * 60 * 60, schedule=next_midnight)
