"""
Service module for the OfficeReportArchitect model.

This module defines the service for handling business logic and exceptions
related to OfficeReportArchitect creation and management.

Classes:
    OfficeReportArchitectService: Service class for OfficeReportArchitect operations.
"""

from collections import defaultdict

from django.db import transaction
from django.utils import timezone

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.core.pagination import CustomPagination
from app.moderation import STATUS_CHOICES
from app.moderation.models import Decision
from app.moderation.models import OfficeReportArchitect
from app.moderation.models import Reason
from app.moderation.serializers import DecisionSerializer
from app.moderation.serializers import OfficeReportArchitectSerializer
from app.moderation.serializers import ReasonSerializer
from app.moderation.services.ReportAction import ARCHITECT_DECISION_ACTION_MAP
from app.users.models import Office


class OfficeReportArchitectService:
    """
    Service class for handling OfficeReportArchitect operations.

    Handles business logic and exception handling for OfficeReportArchitect creation and management.

    Methods:
        create_office_report(request): Handles validation and creation of a new OfficeReportArchitect.
        get_grouped_office_reports(request): Groups reports by architect.
        get_decisions(): Retrieves possible decisions.
        get_reasons(): Retrieves possible reasons.
        change_office_report_status(request, pk): Updates the report status.
        execute_decision(request): Executes a decision on a reported architect.
    """

    pagination_class = CustomPagination

    @classmethod
    def create_office_report(cls, request):
        """
        Handles validation and creation of a new OfficeReportArchitect.
        """
        serializer = OfficeReportArchitectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Extract the reported_architect_id correctly (ensure it's just the id)
        reported_architect = validated_data.pop("reported_architect_id", None)
        if not reported_architect:
            raise APIException(detail="Missing 'reported_architect_id' in request data.")

        user = request.user

        office = Office.objects.get(user=user)

        # Check if a report already exists for the same office and architect
        if OfficeReportArchitect.objects.filter(
            reporting_office=office,
            reported_architect=reported_architect,
            # Ensure we're using the ID here
        ).exists():
            raise APIException(detail="A report for this architect by this office already exists.")

        reasons = validated_data.pop("report_reasons", None)

        with transaction.atomic():
            # Create the new office report with the reported_architect_id as a number
            office_report = OfficeReportArchitect.objects.create(
                reporting_office=office,
                reported_architect=reported_architect,  # Pass the ID here
                **validated_data,  # Pass the rest of the validated data
            )
            office_report.reasons.set(reasons)
            office_report.save()
        return True, OfficeReportArchitectSerializer(office_report).data

    @classmethod
    def get_grouped_office_reports(cls, request):
        """
        Groups OfficeReportArchitect objects by the architect's email and returns them
        as a paginated list.

        Args:
            request (HttpRequest): The incoming HTTP request object containing
            pagination parameters.

        Returns:
            Response: A paginated response containing grouped office reports.
        """
        queryset = OfficeReportArchitect.objects.all()
        office_reports = defaultdict(list)

        for report in queryset:
            architect_email = report.reported_architect.user.email
            office_reports[architect_email].append(OfficeReportArchitectSerializer(report).data)

        grouped_reports = [{architect_email: reports} for architect_email, reports in office_reports.items()]

        paginator = cls.pagination_class()
        page = paginator.paginate_queryset(grouped_reports, request)
        if page is not None:
            return paginator.get_paginated_response(page)

        return Response(grouped_reports, status=status.HTTP_200_OK)

    @classmethod
    def get_decisions(cls):
        """
        Retrieve all possible decisions for OfficeReportArchitect.

        Returns:
            Response: A serialized response containing the list of decisions.
        """
        decisions = Decision.objects.filter(report_type="Office")
        serialized_decisions = DecisionSerializer(decisions, many=True)
        return True, serialized_decisions.data

    @classmethod
    def get_reasons(cls):
        """
        Retrieve all possible reasons for OfficeReportArchitect.

        Returns:
            Response: A serialized response containing the list of reasons.
        """
        reasons = Reason.objects.filter(report_type="Office")
        serialized_reasons = ReasonSerializer(reasons, many=True)
        return True, serialized_reasons.data

    @classmethod
    def change_office_report_status(cls, request, pk):
        """
        Change the status of a specific OfficeReportArchitect.

        Args:
            request (Request): The request object containing the status.
            pk (int): The primary key of the OfficeReportArchitect to update.

        Returns:
            Response: A response object containing the updated report or an error message.
        """
        report = OfficeReportArchitect.objects.get(pk=pk)
        new_status = request.data.get("status")
        if new_status not in dict(STATUS_CHOICES):
            raise serializers.ValidationError(detail="Invalid status choice.")

        report.status = new_status
        report.save()
        return True, OfficeReportArchitectSerializer(report).data

    @classmethod
    def execute_decision(cls, request):
        """
        Executes the decision related to the given OfficeReportArchitect.

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
        action = ARCHITECT_DECISION_ACTION_MAP(decision_id)
        if not action:
            raise serializers.ValidationError("No valid action found for the decision.")

        reports = OfficeReportArchitect.objects.filter(id__in=report_ids)

        action.execute(reports[0].reported_architect, user.admin)

        reports.update(
            status="Treated",
            decision=Decision.objects.get(id=decision_id),
            decision_date=timezone.now(),
        )

        return True, "Decision Executed Successfully."
