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

from background_task import background


from app.announcement.models import Announcement
from app.email_templates.utils import schedule_email_trigger
from app.selection.models.SelectionSettings import SelectionSettings
from app.selection.utils import send_reminder_email
from collections import namedtuple

EmailTriggerParams = namedtuple('EmailTriggerParams', ['model', 'filter_field', 'offset_days', 'action_callback', 'extra_conditions','email_template','extra_action'])

def generate_email_triggers(settings:SelectionSettings):
    """
    Generates a list of email triggers based on provided settings and conditions.
    
    Args:
        settings: The settings object that may contain global configurations for triggers.
    
    Returns:
        List of EmailTriggerParams
    """
    return [
        EmailTriggerParams(
            model=Announcement,
            filter_field="suggested_at",
            offset_days=settings.days_before_call_email,
            action_callback=send_reminder_email,
            extra_conditions={"selections__isnull": True},
            email_template="architect_precall_email.html",
            extra_action=None
        ),

        EmailTriggerParams(
            model=Announcement,
            filter_field="suggested_at",
            offset_days=settings.days_before_call_email+1,
            action_callback=send_reminder_email,
            extra_conditions={"selections__isnull": True},
            email_template="architect_precall_email.html",
            extra_action=None
        ),
        EmailTriggerParams(
            model=Announcement,
            filter_field="suggested_at",
            offset_days=settings.days_before_call_email+settings.days_after_call_email,
            action_callback=send_reminder_email,
            extra_conditions={"selections__isnull": True},
            email_template="architect_postcall_email.html",
            extra_action=None
        ),
        EmailTriggerParams(
            model=Announcement,
            filter_field="suggested_at",
            offset_days=settings.days_to_rediffuse,
            action_callback=send_reminder_email,
            extra_conditions={"selections__isnull": True},
            email_template="architect_broadcast_email.html",
            extra_action=broadcast_announcement
        ),
        EmailTriggerParams(
            model=Announcement,
            filter_field="suggested_at",
            offset_days=settings.phase_days,
            action_callback=send_reminder_email,
            extra_conditions={"selections__isnull": True},
            email_template="architect_block_email.html",
            extra_action=bloc_announcement
        ),
    ]
    

def broadcast_announcement(announcement:Announcement):
    """
    Resets the architect association for an Announcement instance.

    Args:
        announcement (Announcement): The Announcement instance to modify.

    """
    announcement.architect=None
    announcement.save()

def bloc_announcement(announcement:Announcement):
    """
    Blocks an Announcement instance.

    Args:
        announcement (Announcement): The Announcement instance to block.

    """
    announcement.is_blocked=True
    announcement.save() 

@background(schedule=0)
def process_email_triggers():
    """
    Periodically checks and triggers email notifications based on date conditions.
    """
    try:
        settings = SelectionSettings.objects.first()
        if not settings:
            print("No SelectionSettings found. Exiting...")
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
                extra_action=trigger.extra_action
            )

    except Exception as e:
        print(f"Error in process_email_triggers: {e}")