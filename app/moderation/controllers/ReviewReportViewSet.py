"""
ViewSet module for the ReviewReport model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.moderation.controllers.ManageReportingPermission import ManageReportingPermission
from app.moderation.models.ReviewReport import ReviewReport
from app.moderation.serializers.ReviewReportSerializer import ReviewReportSerializer
from app.moderation.services.ReviewReportService import ReviewReportService


class ReviewReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ReviewReport model.
    """

    queryset = ReviewReport.objects.all()
    serializer_class = ReviewReportSerializer

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

    def create(self, request, *args, **kwargs):
        """
        Override the create method to use ReviewReportService for handling the creation
        of a ReviewReport.
        """
        return ReviewReportService.create_review_report(request)

    @action(detail=False)
    def get_decisions(self, request):
        """
        Retrieve all possible decisions for the corresponding type.
        """
        return ReviewReportService.get_decisions()

    @action(detail=False)
    def get_reasons(self, request):
        """
        Retrieve all possible reasons for the corresponding type.
        """
        return ReviewReportService.get_reasons()

    @action(detail=True)
    def change_status(self, request, pk=None):
        """
        Change the status of an ReviewReport.
        """
        return ReviewReportService.change_architect_report_status(request, pk)

    @action(detail=True)
    def execute_decision(self, request, pk=None):
        """
        Execute decision of an ReviewReport.
        """
        return ReviewReportService.execute_decision(request, pk)
