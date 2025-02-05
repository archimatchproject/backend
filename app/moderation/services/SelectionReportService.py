"""
Service module for the ArchitectReport model.

This module defines the service for handling the business logic and exceptions
related to ArchitectReport creation and management.

Classes:
    ArchitectReportService: Service class for ArchitectReport operations.
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
from app.moderation.models.Reason import Reason
from app.moderation.serializers.ArchitectReportSerializer import (
    ArchitectReportSerializer,
)
from app.moderation.serializers.DecisionSerializer import DecisionSerializer
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.moderation.services.ReportAction import SELECTION_DECISION_ACTION_MAP
from app.users.models.Client import Client
from app.moderation.serializers.SelectionReportSerializer import (
    SelectionReportSerializer,
)
from app.moderation.models.SelectionReport import SelectionReport


class SelectionReportService:
    """
    Service class for handling ArchitectReport operations.

    Handles business logic and exception handling for ArchitectReport creation and management.

    Methods:
        create_architect_report(request): Handles validation and creation of a new ArchitectReport.
    """

    pagination_class = CustomPagination

    @classmethod
    def create_selection_report(cls, request):
        """
        Handles validation and creation of a new SelectionReport.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = SelectionReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            client = Client.objects.get(user=user)
            reasons = validated_data.pop("report_reasons")
            print("reasons", reasons)
            with transaction.atomic():
                # Create SelectionReport instance
                selection_report = SelectionReport.objects.create(
                    reporting_client=client,
                    selection=validated_data.pop("selection_id"),
                    **validated_data,
                )
                selection_report.reasons.set(reasons)
                selection_report.save()
                return True, ArchitectReportSerializer(selection_report).data

        except IntegrityError as e:
            if "unique constraint" in str(e):
                raise serializers.ValidationError(
                    {
                        "detail": "A report for this architect by this client already exists."
                    }
                )
            raise APIException(detail=f"Error creating architect report: {str(e)}")
        except Client.DoesNotExist:
            raise NotFound(detail="Authenticated user is not a client.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating architect report: {str(e)}")

    @classmethod
    def get_grouped_selection_reports(cls, request):
        """
        Handle GET request and return paginated selection reports.

        This method retrieves all selection reports and applies pagination based on the request
        parameters.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the selection reports, or an error message if
                      the data retrieval fails.

        Raises:
            APIException: If there is an issue with data retrieval or processing.
        """
        try:
            queryset = SelectionReport.objects.all().order_by("-created_at")
            paginator = cls.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = SelectionReportSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            return Response(
                {"message": "error retrieving data"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            raise APIException(f"Error retrieving selection reports: {str(e)}")

    @classmethod
    def get_decisions(cls):
        """
        Retrieve all possible decisions for the corresponding type and return as a serialized
          Response.

        Returns:
            Response: A serialized response containing the list of decisions.
        """
        decisions = Decision.objects.filter(report_type="Selection")
        serialized_decisions = DecisionSerializer(decisions, many=True)
        return True, serialized_decisions.data

    @classmethod
    def get_reasons(cls):
        """
        Retrieve all possible reasons for the corresponding type and return as a serialized
          Response.

        Returns:
            Response: A serialized response containing the list of reasons.
        """
        reasons = Reason.objects.filter(report_type="Selection")
        serialized_reasons = ReasonSerializer(reasons, many=True)
        return True, serialized_reasons.data

    @classmethod
    def change_selection_report_status(cls, request, pk):
        """
        Change the status of a specific SelectionReport.

        Args:
            request (Request): The request object containing the status.
            pk (int): The primary key of the ArchitectReport to update.

        Returns:
            Response: A response object containing the updated report or an error message.
        """

        report = SelectionReport.objects.get(pk=pk)
        new_status = request.data.get("status")
        if new_status not in dict(STATUS_CHOICES):
            raise serializers.ValidationError(detail="Invalid status choice.")

        report.status = new_status
        report.save()
        return True, SelectionReportSerializer(report).data

    @classmethod
    def execute_decision(cls, request):
        """
        Executes the decision related to the given SelectionReport.

        Parameters:
        - request: The request object containing the decision data.

        Returns:
        - A Response object indicating the result of the operation.
        """
        print(request.data)
        report_ids = request.data.get("report_ids", [])
        decision_id = request.data.get("decision_id")
        user = request.user
        print("aaaaaaaaaaaaaaaaaaaaaa", report_ids, decision_id)
        if not report_ids or not decision_id:
            raise serializers.ValidationError(
                detail="Report IDs and Decision ID are required."
            )
        action = SELECTION_DECISION_ACTION_MAP.get(decision_id)
        if not action:
            raise serializers.ValidationError("No valid action found for the decision.")

        reports = SelectionReport.objects.filter(id__in=report_ids)

        action.execute(reports[0].selection, user.admin)

        reports.update(
            status="Treated",
            decision=Decision.objects.get(id=decision_id),
            decision_date=timezone.now(),
        )

        return True, "Decision Executed Successfully."
