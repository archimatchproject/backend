"""

This module is responsible for generating and scheduling email triggers based on specified
conditions, including date offsets, filters, and callbacks. It integrates background task
processing using the `django-background-tasks` library to ensure email triggers are handled
asynchronously.


Functions:
    generate_email_triggers: Creates a list of email trigger configurations.
    broadcast_announcement: Resets the architect association for an Announcement instance.
    bloc_announcement: Blocks an Announcement instance.
    process_email_triggers: Periodically triggers emails based on date conditions.

"""

from collections import namedtuple

from background_task import background

from app.email_templates.utils import schedule_email_trigger
from app.selection import DISCUSSION
from app.selection.models.Selection import Selection
from app.selection.models.SelectionSettings import SelectionSettings
from app.selection.utils import send_reminder_discussion_email
from app.selection.utils import send_reminder_email


EmailTriggerParams = namedtuple(
    "EmailTriggerParams",
    [
        "model",
        "filter_field",
        "offset_days",
        "action_callback",
        "extra_conditions",
        "email_template",
        "extra_action",
    ],
)


def generate_email_triggers(settings: SelectionSettings):
    """
    Generates a list of email triggers based on provided settings and conditions.

    Args:
        settings: The settings object that may contain global configurations for triggers.

    Returns:
        List of EmailTriggerParams
    """
    return [
        EmailTriggerParams(
            model=Selection,
            filter_field="phase__start_date",
            offset_days=settings.days_before_call_email - 1,
            action_callback=send_reminder_discussion_email,
            extra_conditions={"phase__number": 1},
            email_template="architect_discussion_before_call.html",
            extra_action=None,
        ),
        EmailTriggerParams(
            model=Selection,
            filter_field="phase__start_date",
            offset_days=settings.days_before_call_email,
            action_callback=send_reminder_discussion_email,
            extra_conditions={"phase__number": 1},
            email_template="architect_discussion_call.html",
            extra_action=None,
        ),
        EmailTriggerParams(
            model=Selection,
            filter_field="phase__start_date",
            offset_days=settings.days_before_call_email + 2,
            action_callback=send_reminder_discussion_email,
            extra_conditions={"phase__number": 1},
            email_template="architect_discussion_before_call.html",
            extra_action=None,
        ),
        EmailTriggerParams(
            model=Selection,
            filter_field="phase__start_date",
            offset_days=settings.phase_days,
            action_callback=send_reminder_email,
            extra_conditions={"phase__number": 1},
            email_template="architect_discussion_block_email.html",
            extra_action=bloc_selection,
        ),
    ]


def bloc_selection(selection: Selection):
    """
    Blocks an selection instance.

    Args:
        selection (Selection): The selection instance to block.

    """
    selection.is_blocked = True
    selection.save()


@background(schedule=0)
def process_email_discussion_triggers():
    """
    Periodically checks and triggers email notifications based on date conditions.
    """
    try:
        settings = SelectionSettings.objects.filter(name=DISCUSSION).first()
        if not settings:
            return

        email_triggers = generate_email_triggers(settings)

        for trigger in email_triggers:
            schedule_email_trigger(
                model=trigger.model,
                filter_field=trigger.filter_field,
                offset_days=trigger.offset_days,
                action_callback=trigger.action_callback,
                extra_conditions=trigger.extra_conditions,
                email_template=trigger.email_template,
                extra_action=trigger.extra_action,
            )

    except Exception:
        pass
