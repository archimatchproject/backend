from app.selection.utils import generate_choices

ACCEPTED = "Accepted"
REFUSED = "Refused"
INTERESTED = "Interested"
SELECTION_STATUS_CHOICES = [
    (ACCEPTED, ACCEPTED),
    (REFUSED, REFUSED),
    (INTERESTED, INTERESTED),
]


DISCUSSION = "Discussion"
QUOTES = "Quotes"
DECISION = "Decision"
NOT_SELECTED = "Not Selected"

# Choices for the phase names
PHASE_NAME_CHOICES = [
    (DISCUSSION, DISCUSSION),
    (QUOTES, QUOTES),
    (DECISION, DECISION),
    (NOT_SELECTED, NOT_SELECTED),
]

QUOTE_PENDING = "Pending"
QUOTE_ACCEPTED = "Accepted"
QUOTE_REFUSED = "Refused"
QUOTE_STATUS_CHOICES = [
    (QUOTE_PENDING, QUOTE_PENDING),
    (QUOTE_ACCEPTED, QUOTE_ACCEPTED),
    (QUOTE_REFUSED, QUOTE_REFUSED),
]


PHASE_DAYS_CHOICES = generate_choices(7, 10, "{value} jours")
DAYS_BEFORE_CALL_EMAIL_CHOICES = generate_choices(2, 5, "pendant {value} jours")
DAYS_TO_PHONE_CALL_CHOICES = generate_choices(2, 5, "après {value} jours")
DAYS_AFTER_CALL_EMAIL_CHOICES = generate_choices(1, 5, "pendant {value} jours")
DAYS_TO_REDIFFUSE_CHOICES = generate_choices(7, 9, "aprés {value} jours")
DAYS_TO_LOCK_PROJECT_CHOICES = generate_choices(1, 3, "après {value} jours")
TIMES_TO_UNLOCK_PROJECT_CHOICES = generate_choices(1, 3, "{value} fois")
DAYS_FOR_ADMIN_MANAGEMENT_CHOICES = generate_choices(10, 15, "apres {value} jours")
DAYS_FOR_ADMIN_DISPLAY_CHOICES = generate_choices(3, 7, "après {value} jours")


CHANGE_DEADLINE = "Change deadline"
CANCEL_PROJECT = "Cancel the project"
BLOCK_PROJECT = "Block the project"
REBROADCAST_PROJECT = "Rebroadcast the project"
CONFIRM_DISCUSSION_PHASE = "Confirm discussion phase"

ACTION_CHOICES = [
    (CHANGE_DEADLINE, CHANGE_DEADLINE),
    (CANCEL_PROJECT, CANCEL_PROJECT),
    (BLOCK_PROJECT, BLOCK_PROJECT),
    (REBROADCAST_PROJECT, REBROADCAST_PROJECT),
    (CONFIRM_DISCUSSION_PHASE, CONFIRM_DISCUSSION_PHASE),
]
