"""
Module for handling report actions.

This module defines an abstract base class `BaseAction` and specific action
classes for various types of reports, including architect reports, client reviews,
and project reports. Each action class implements the `execute` method to perform
the specific action logic associated with a decision.
"""

from abc import ABC
from abc import abstractmethod
from datetime import date
from datetime import timedelta

from app.email_templates.signals import api_success_signal
from app.moderation.models.Warning import Warning
from project_core.django import base as settings


class BaseAction(ABC):
    """
    Abstract base class for all report actions.

    This class should be inherited by specific action classes that define the logic
    for handling various decisions related to reports.

    Attributes:
        report (object): The report instance that the action is associated with.
    """

    def __init__(self, report):
        """
        Initialize the action with a report instance.

        Args:
            report (object): The report instance associated with the action.
        """
        self.report = report

    @abstractmethod
    def execute(reported, admin):
        """
        Execute the action associated with this decision.
        This method should be implemented by subclasses to define the specific
        logic for each action.
        """
        pass


# -------------------------------------------------------------------------------------------------
# Actions for Architect Reports
# -------------------------------------------------------------------------------------------------


class AdresserAvertissementArchitect(BaseAction):
    """
    Action to address a warning to an architect.

    This class implements the logic to issue a warning to an architect based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action to address a warning to an architect.
        """
        Warning.objects.create(issued_by=admin, issued_for=reported.user)
        architect = reported.user

        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        signal_data = {
            "template_name": "warn_architect.html",
            "context": {
                "first_name": architect.first_name,
                "last_name": architect.last_name,
                "email": architect.email,
            },
            "to_email": architect.email,
            "subject": "Warning: Avertissement concernant votre compte sur Archimatch",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


class SuspendreTemporairement(BaseAction):
    """
    Action to temporarily suspend an architect.

    This class implements the logic to temporarily suspend an architect based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action to temporarily suspend an architect.
        """
        architect = reported.user
        architect.is_suspended = True
        architect.suspension_start_date = date.today()
        architect.suspension_end_date = date.today() + timedelta(days=30)  # Example: 30 days suspension
        architect.save()

        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        signal_data = {
            "template_name": "suspendre_temporairement_architect.html",
            "context": {
                "first_name": architect.first_name,
                "last_name": architect.last_name,
                "email": architect.email,
                "end_date": architect.suspension_end_date,
            },
            "to_email": architect.email,
            "subject": "Warning: Suspension temporaire de votre compte sur Archimatch",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


class SuspendreDefinitivement(BaseAction):
    """
    Action to permanently suspend an architect.

    This class implements the logic to permanently suspend an architect based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action to permanently suspend an architect.
        """
        architect = reported.user
        architect.is_suspended = True
        architect.suspension_start_date = date.today
        architect.suspension_end_date = None
        architect.save()

        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        architect = reported.architect
        signal_data = {
            "template_name": "suspend_definitively_architect.html",
            "context": {
                "first_name": architect.user.first_name,
                "last_name": architect.user.last_name,
                "email": architect.user.email,
            },
            "to_email": architect.user.email,
            "subject": "Warning: Suspension définitive de votre compte sur Archimatch",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


# -------------------------------------------------------------------------------------------------
# Actions for Client Reviews
# -------------------------------------------------------------------------------------------------


class ReviewAdresserAvertissementClient(BaseAction):
    """
    Action to address a warning to a client.

    This class implements the logic to issue a warning to a client based on a review report.
    """

    def execute(reported, admin):
        """
        Execute the action to address a warning to a client.
        """
        """
        Execute the action to address a warning to an architect.
        """
        Warning.objects.create(issued_by=admin, issued_for=reported.client.user)

        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        client = reported.client
        signal_data = {
            "template_name": "warn_client.html",
            "context": {
                "first_name": client.user.first_name,
                "last_name": client.user.last_name,
                "email": client.user.email,
            },
            "to_email": client.user.email,
            "subject": "Warning: Avertissement concernant votre compte sur Archimatch",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


class SuppressionAvis(BaseAction):
    """
    Action to delete a review.

    This class implements the logic to delete a client review based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action to delete a review.
        """
        client = reported.client
        architect = reported.architect
        reported.delete()
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES

        signal_data = {
            "template_name": "delete_review_client.html",
            "context": {
                "first_name": client.user.first_name,
                "last_name": client.user.last_name,
                "email": client.user.email,
                "architect_first_name": architect.user.first_name,
                "architect_last_name": architect.user.last_name,
            },
            "to_email": client.user.email,
            "subject": "Concernant votre avis sur Archimatch",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


class ConservationAvis(BaseAction):
    """
    Action to keep a review.

    This class implements the logic to keep a client review based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action to keep a review.
        """
        client = reported.client
        architect = reported.reporting_architect
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES

        signal_data = {
            "template_name": "keep_review_client.html",
            "context": {
                "first_name": client.user.first_name,
                "last_name": client.user.last_name,
                "email": client.user.email,
                "architect_first_name": architect.user.first_name,
                "architect_last_name": architect.user.last_name,
            },
            "to_email": client.user.email,
            "subject": "Concernant votre avis sur Archimatch",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


# -------------------------------------------------------------------------------------------------
# Actions for Project Reports
# -------------------------------------------------------------------------------------------------
class ProjectAdresserAvertissementClient(BaseAction):
    """
    Action to address a warning to a client.

    This class implements the logic to issue a warning to a client based on a review report.
    """

    def execute(reported, admin):
        """
        Execute the action to address a warning to a client.
        """
        """
        Execute the action to address a warning to an architect.
        """
        Warning.objects.create(issued_by=admin, issued_for=reported.client.user)

        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        client = reported.client
        signal_data = {
            "template_name": "warn_client.html",
            "context": {
                "first_name": client.user.first_name,
                "last_name": client.user.last_name,
                "email": client.user.email,
            },
            "to_email": client.user.email,
            "subject": "Warning: Architect Project Selection",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


class SuppressionProjet(BaseAction):
    """
    Action to delete a project.

    This class implements the logic to delete a project based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action to delete a project.
        """
        client = reported.client
        reported.delete()
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        signal_data = {
            "template_name": "delete_project_client.html",
            "context": {
                "first_name": client.user.first_name,
                "last_name": client.user.last_name,
                "email": client.user.email,
            },
            "to_email": client.user.email,
            "subject": "Warning: Suppression de votre projet",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


class ConservationProjet(BaseAction):
    """
    Action to keep a project.

    This class implements the logic to keep a project based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action to keep a project.
        """
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        client = reported.client
        signal_data = {
            "template_name": "warn_client.html",
            "context": {
                "first_name": client.user.first_name,
                "last_name": client.user.last_name,
                "email": client.user.email,
            },
            "to_email": client.user.email,
            "subject": "Warning: Architect Project Selection",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


# -------------------------------------------------------------------------------------------------
# Actions for Selection Reports
# -------------------------------------------------------------------------------------------------
class AddressWarningArchitect(BaseAction):
    """
    Action to address a warning to an architect.

    This class implements the logic to issue a warning to an architect based on a review report.
    """

    def execute(reported, admin):
        """
        Execute the action to address a warning to an architect.
        """
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        architect = reported.architect
        signal_data = {
            "template_name": "architect_warning_email.html",
            "context": {
                "first_name": architect.user.first_name,
                "last_name": architect.user.last_name,
                "email": architect.user.email,
            },
            "to_email": architect.user.email,
            "subject": "Warning: Architect Project Selection",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)
        Warning.objects.create(issued_by=admin, issued_for=reported.architect.user)


class BlockSelection(BaseAction):
    """
    Action to block a selection.

    This class implements the logic to block a selection based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action to block a selection.
        """
        reported.is_blocked = True
        reported.save()
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        architect = reported.architect
        signal_data = {
            "template_name": "architect_block_project_email.html",
            "context": {
                "first_name": architect.user.first_name,
                "last_name": architect.user.last_name,
                "email": architect.user.email,
            },
            "to_email": architect.user.email,
            "subject": "Warning: Architect Project Selection",
            "images": email_images,
        }
        api_success_signal.send(sender=None, data=signal_data)


# -------------------------------------------------------------------------------------------------
# No Action
# -------------------------------------------------------------------------------------------------


class NoAction(BaseAction):
    """
    No action to be taken.

    This class represents a decision where no action is required based on a report.
    """

    def execute(reported, admin):
        """
        Execute the action for no action required.
        """


ARCHITECT_DECISION_ACTION_MAP = {
    1: AdresserAvertissementArchitect,
    2: SuspendreTemporairement,
    3: SuspendreDefinitivement,
    4: NoAction,
}

REVIEW_DECISION_ACTION_MAP = {
    5: ReviewAdresserAvertissementClient,
    6: SuppressionAvis,
    7: ConservationAvis,
    8: NoAction,
}

PROJECT_DECISION_ACTION_MAP = {
    9: ProjectAdresserAvertissementClient,
    10: SuppressionProjet,
    11: ConservationProjet,
    12: NoAction,
}

SELECTION_DECISION_ACTION_MAP = {
    13: AddressWarningArchitect,
    14: BlockSelection,
}
