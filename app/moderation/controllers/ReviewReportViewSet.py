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
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

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

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Override the create method to use ReviewReportService for handling the creation
        of a ReviewReport.
        """
        success,data = ReviewReportService.create_review_report(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)


    @action(detail=False)
    @handle_service_exceptions
    def get_decisions(self, request):
        """
        Retrieve all possible decisions for the corresponding type.
        """
        success,data = ReviewReportService.get_decisions()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False)
    @handle_service_exceptions
    def get_reasons(self, request):
        """
        Retrieve all possible reasons for the corresponding type.
        """
        success,data = ReviewReportService.get_reasons()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=True)
    @handle_service_exceptions
    def change_status(self, request, pk=None):
        """
        Change the status of an ReviewReport.
        """
        success,data = ReviewReportService.change_architect_report_status(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(detail=True)
    @handle_service_exceptions
    def execute_decision(self, request, pk=None):
        """
        Execute decision of an ReviewReport.
        """
        success,data = ReviewReportService.execute_decision(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @handle_service_exceptions
    def list(self,request):
        return ReviewReportService.review_reports_get_all(request)