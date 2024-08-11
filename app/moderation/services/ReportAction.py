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

from app.moderation.models.Warning import Warning


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
    def execute(report, admin):
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

    def execute(report, admin):
        """
        Execute the action to address a warning to an architect.
        """
        Warning.objects.create(issued_by=admin.admin, issued_for=report.reported_architect.user)
        report.status = "Treated"
        report.save()


class SuspendreTemporairement(BaseAction):
    """
    Action to temporarily suspend an architect.

    This class implements the logic to temporarily suspend an architect based on a report.
    """

    def execute(report, admin):
        """
        Execute the action to temporarily suspend an architect.
        """
        architect = report.reported_architect.user
        architect.is_suspended = True
        architect.suspension_start_date = date.today()
        architect.suspension_end_date = date.today() + timedelta(
            days=30
        )  # Example: 30 days suspension
        architect.save()


class SuspendreDefinitivement(BaseAction):
    """
    Action to permanently suspend an architect.

    This class implements the logic to permanently suspend an architect based on a report.
    """

    def execute(report, admin):
        """
        Execute the action to permanently suspend an architect.
        """
        architect = report.reported_architect.user
        architect.is_suspended = True
        architect.suspension_start_date = date.today
        architect.suspension_end_date = None
        architect.save()


# -------------------------------------------------------------------------------------------------
# Actions for Client Reviews
# -------------------------------------------------------------------------------------------------


class ReviewAdresserAvertissementClient(BaseAction):
    """
    Action to address a warning to a client.

    This class implements the logic to issue a warning to a client based on a review report.
    """

    def execute(report, admin):
        """
        Execute the action to address a warning to a client.
        """
        """
        Execute the action to address a warning to an architect.
        """
        Warning.objects.create(issued_by=admin.admin, issued_for=report.reported_review.client.user)
        report.status = "Treated"
        report.save()


class SuppressionAvis(BaseAction):
    """
    Action to delete a review.

    This class implements the logic to delete a client review based on a report.
    """

    def execute(report, admin):
        """
        Execute the action to delete a review.
        """

        report.reported_review.delete()
        report.status = "Treated"
        report.save()


class ConservationAvis(BaseAction):
    """
    Action to keep a review.

    This class implements the logic to keep a client review based on a report.
    """

    def execute(report, admin):
        """
        Execute the action to keep a review.
        """

        report.status = "Treated"
        report.save()


# -------------------------------------------------------------------------------------------------
# Actions for Project Reports
# -------------------------------------------------------------------------------------------------
class ProjectAdresserAvertissementClient(BaseAction):
    """
    Action to address a warning to a client.

    This class implements the logic to issue a warning to a client based on a review report.
    """

    def execute(report, admin):
        """
        Execute the action to address a warning to a client.
        """
        """
        Execute the action to address a warning to an architect.
        """
        Warning.objects.create(
            issued_by=admin.admin, issued_for=report.reported_project.client.user
        )
        report.status = "Treated"
        report.save()


class SuppressionProjet(BaseAction):
    """
    Action to delete a project.

    This class implements the logic to delete a project based on a report.
    """

    def execute(report, admin):
        """
        Execute the action to delete a project.
        """

        report.reported_project.delete()
        report.status = "Treated"
        report.save()


class ConservationProjet(BaseAction):
    """
    Action to keep a project.

    This class implements the logic to keep a project based on a report.
    """

    def execute(report, admin):
        """
        Execute the action to keep a project.
        """

        report.status = "Treated"
        report.save()


# -------------------------------------------------------------------------------------------------
# No Action
# -------------------------------------------------------------------------------------------------


class NoAction(BaseAction):
    """
    No action to be taken.

    This class represents a decision where no action is required based on a report.
    """

    def execute(report, admin):
        """
        Execute the action for no action required.
        """
        report.status = "Treated"
        report.save()


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
