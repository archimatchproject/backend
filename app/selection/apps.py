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
        """
        This method is called when the application is ready.
        It schedules the `process_email_triggers` task to run daily at midnight if it is not already scheduled.
        The task is scheduled to run at the next midnight in the UTC timezone.
        The following tasks are checked and scheduled if not already present:
        - `process_email_triggers`
        - `process_email_discussion_triggers`
        - `process_email_quote_triggers`
        Imports:
            datetime: To get the current time and calculate the next midnight.
            timedelta: To add a day to the current time.
            pytz: To set the timezone to UTC.
            Task: To check if the task is already scheduled.
            process_email_triggers: The task to be scheduled.
        Variables:
            timezone: The UTC timezone.
            now: The current time in UTC.
            next_midnight: The next midnight time in UTC.
        """

        # Schedule the task if not already scheduled
        from datetime import datetime
        from datetime import timedelta

        import pytz

        from background_task.models import Task

        from app.selection.tasks.selection_phase_tasks import process_email_triggers

        timezone = pytz.timezone("UTC")
        now = datetime.now(timezone)
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        if not Task.objects.filter(
            task_name="app.selection.tasks.selection_phase_tasks.process_email_triggers"
        ).exists():
            process_email_triggers(repeat=24 * 60 * 60, schedule=next_midnight)
        if not Task.objects.filter(
            task_name="app.selection.tasks.selection_phase_tasks.process_email_discussion_triggers"
        ).exists():
            process_email_triggers(repeat=24 * 60 * 60, schedule=next_midnight)
        if not Task.objects.filter(
            task_name="app.selection.tasks.selection_phase_tasks.process_email_quote_triggers"
        ).exists():
            process_email_triggers(repeat=24 * 60 * 60, schedule=next_midnight)

