"""
Service module for the ProjectReport model.

This module defines the service for handling the business logic and exceptions
related to ProjectReport creation and management.

Classes:
    ProjectReportService: Service class for ProjectReport operations.
"""

from django.db import IntegrityError
from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.moderation.models.Decision import Decision
from app.moderation.models.ProjectReport import ProjectReport
from app.moderation.models.Reason import Reason
from app.moderation.serializers.DecisionSerializer import DecisionSerializer
from app.moderation.serializers.ProjectReportSerializer import ProjectReportSerializer
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.users.models.Architect import Architect


class ProjectReportService:
    """
    Service class for handling ProjectReport operations.

    Handles business logic and exception handling for ProjectReport creation and management.

    Methods:
        create_project_report(request): Handles validation and creation of a new ProjectReport.
    """

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
                return Response(
                    ProjectReportSerializer(project_report).data,
                    status=status.HTTP_201_CREATED,
                )
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
        return Response(serialized_decisions.data)

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
        return Response(serialized_reasons.data)
