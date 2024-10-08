"""
Service module for the ProjectReport model.

This module defines the service for handling the business logic and exceptions
related to ProjectReport creation and management.

Classes:
    ProjectReportService: Service class for ProjectReport operations.
"""

from django.db import IntegrityError
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.core.pagination import CustomPagination
from app.moderation import STATUS_CHOICES
from app.moderation.models.Decision import Decision
from app.moderation.models.ProjectReport import ProjectReport
from app.moderation.models.Reason import Reason
from app.moderation.serializers.DecisionSerializer import DecisionSerializer
from app.moderation.serializers.ProjectReportSerializer import ProjectReportSerializer
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.moderation.services.ReportAction import PROJECT_DECISION_ACTION_MAP
from app.users.models.Architect import Architect


class ProjectReportService:
    """
    Service class for handling ProjectReport operations.

    Handles business logic and exception handling for ProjectReport creation and management.

    Methods:
        create_project_report(request): Handles validation and creation of a new ProjectReport.
    """
    pagination_class = CustomPagination
    @classmethod
    def create_project_report(cls, request):
        """
        Handles validation and creation of a new ProjectReport.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ProjectReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            architect = Architect.objects.get(user=user)
            reasons = validated_data.pop("reasons")
            with transaction.atomic():
                # Create ProjectReport instance
                project_report = ProjectReport.objects.create(
                    reporting_architect=architect,
                    reported_project=validated_data.pop("reported_project_id"),
                    **validated_data,
                )
                project_report.reasons.set(reasons)
                project_report.save()
                return True,ProjectReportSerializer(project_report).data
        except IntegrityError as e:
            if "unique constraint" in str(e):
                raise serializers.ValidationError(
                    {"detail": "A report for this project by this architect already exists."}
                )
            raise APIException(detail=f"Error creating project report: {str(e)}")
        except Architect.DoesNotExist:
            raise NotFound(detail="Authenticated user is not an architect.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating project report: {str(e)}")

    @classmethod
    def get_decisions(cls):
        """
        Retrieve all possible decisions for the corresponding type and return as a serialized
          Response.

        Returns:
            Response: A serialized response containing the list of decisions.
        """
        decisions = Decision.objects.filter(report_type="Project")
        serialized_decisions = DecisionSerializer(decisions, many=True)
        return True,serialized_decisions.data

    @classmethod
    def get_reasons(cls):
        """
        Retrieve all possible reasons for the corresponding type and return as a serialized
          Response.

        Returns:
            Response: A serialized response containing the list of reasons.
        """
        reasons = Reason.objects.filter(report_type="Project")
        serialized_reasons = ReasonSerializer(reasons, many=True)
        return True,serialized_reasons.data

    @classmethod
    def change_architect_report_status(cls, request, pk):
        """
        Change the status of a specific ProjectReport.

        Args:
            request (Request): The request object containing the status.
            pk (int): The primary key of the ProjectReport to update.

        Returns:
            Response: A response object containing the updated report or an error message.
        """

        report = ProjectReport.objects.get(pk=pk)
        new_status = request.data.get("status")
        if new_status not in dict(STATUS_CHOICES):
            raise serializers.ValidationError(detail="Invalid status choice.")

        report.status = new_status
        report.save()
        return True,ProjectReportSerializer(report).data
    
    @classmethod
    def execute_decision(cls, request):
        """
        Executes the decision related to the given ProjectReport.

        Parameters:
        - request: The request object containing the decision data.

        Returns:
        - A Response object indicating the result of the operation.
        """

        report_ids = request.data.get("report_ids", [])
        decision_id = request.data.get("decision_id")
        user = request.user


        if not report_ids or not decision_id:
            raise serializers.ValidationError(detail="Report IDs and Decision ID are required.")

        action = PROJECT_DECISION_ACTION_MAP.get(decision_id)
        if not action:
            raise serializers.ValidationError("No valid action found for the decision.")

        reports = ProjectReport.objects.filter(id__in=report_ids)
        action.execute(reports[0].reported_project, user.admin)
        reports.update(
            status="Treated",
            decision=Decision.objects.get(id=decision_id),
            decision_date=timezone.now(),
        )

        return True,"Decision Executed Successfully."

    @classmethod
    def project_reports_get_all(cls, request):
        """
        Handle GET request and return paginated ProjectReport objects.
        This method retrieves all ProjectReport objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination parameters are not provided correctly or if an
        error occurs during serialization or database access, it returns a 400 Bad
        Request response with an appropriate error message.
        Args:
            request (HttpRequest): The incoming HTTP request object containing
                pagination parameters like page number, page size, etc.
        Returns:
            Response: A paginated response containing serialized ProjectReport objects
                or a 400 Bad Request response with an error message.
        """

        queryset = ProjectReport.objects.all()

        # Instantiate the paginator
        paginator = cls.pagination_class()

        # Apply pagination to the filtered queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProjectReportSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ProjectReportSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)