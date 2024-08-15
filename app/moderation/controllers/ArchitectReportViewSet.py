"""
ViewSet module for the ArchitectReport model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.moderation.controllers.ManageReportingPermission import ManageReportingPermission
from app.moderation.models.ArchitectReport import ArchitectReport
from app.moderation.serializers.ArchitectReportSerializer import ArchitectReportSerializer
from app.moderation.services.ArchitectReportService import ArchitectReportService


class ArchitectReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ArchitectReport model.
    """

    queryset = ArchitectReport.objects.all()
    serializer_class = ArchitectReportSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["create", "get_reasons"]:
            return [IsAuthenticated()]
        elif self.action in [
            "update",
            "partial_update",
            "destroy",
            "list",
            "retrieve",
            "get_decisions",
            "change_status",
            "execute_decision",
        ]:
            return [IsAuthenticated(), ManageReportingPermission()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """
        Override the list method to return grouped ArchitectReport objects.
        """
        return ArchitectReportService.get_grouped_architect_reports()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to use ArchitectReportService for handling the creation
        of an ArchitectReport.
        """
        return ArchitectReportService.create_architect_report(request)

    @action(detail=False)
    def get_decisions(self, request):
        """
        Retrieve all possible decisions for the corresponding type.
        """
        return ArchitectReportService.get_decisions()

    @action(detail=False)
    def get_reasons(self, request):
        """
        Retrieve all possible reasons for the corresponding type.
        """
        return ArchitectReportService.get_reasons()

    @action(detail=True)
    def change_status(self, request, pk=None):
        """
        Change the status of an ArchitectReport.
        """
        return ArchitectReportService.change_architect_report_status(request, pk)

    @action(detail=True)
    def execute_decision(self, request):
        """
        Execute a decision on multiple architect reports.

        This method processes the decision for the provided report IDs.
        """
        return ArchitectReportService.execute_decision(request)
