"""
ViewSet module for the ProjectReport model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.moderation.controllers.ManageReportingPermission import ManageReportingPermission
from app.moderation.models.ProjectReport import ProjectReport
from app.moderation.serializers.ProjectReportSerializer import ProjectReportSerializer
from app.moderation.services.ProjectReportService import ProjectReportService


class ProjectReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProjectReport model.
    """

    queryset = ProjectReport.objects.all()
    serializer_class = ProjectReportSerializer

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
        ]:
            return [IsAuthenticated(), ManageReportingPermission()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to use ProjectReportService for handling the creation
        of a ProjectReport.
        """
        return ProjectReportService.create_project_report(request)

    @action(detail=False, methods=["get"], url_path="decisions")
    def get_decisions(self, request):
        """
        Retrieve all possible decisions for the corresponding type.
        """
        return ProjectReportService.get_decisions()

    @action(detail=False, methods=["get"], url_path="reasons")
    def get_reasons(self, request):
        """
        Retrieve all possible reasons for the corresponding type.
        """
        return ProjectReportService.get_reasons()
