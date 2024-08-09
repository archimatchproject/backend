"""
Service module for the ArchitectReport model.

This module defines the service for handling the business logic and exceptions
related to ArchitectReport creation and management.

Classes:
    ArchitectReportService: Service class for ArchitectReport operations.
"""

from collections import defaultdict

from django.db import IntegrityError
from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.moderation import STATUS_CHOICES
from app.moderation.models.ArchitectReport import ArchitectReport
from app.moderation.models.Decision import Decision
from app.moderation.models.Reason import Reason
from app.moderation.serializers.ArchitectReportSerializer import ArchitectReportSerializer
from app.moderation.serializers.DecisionSerializer import DecisionSerializer
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.users.models.Client import Client


class ArchitectReportService:
    """
    Service class for handling ArchitectReport operations.

    Handles business logic and exception handling for ArchitectReport creation and management.

    Methods:
        create_architect_report(request): Handles validation and creation of a new ArchitectReport.
    """

    @classmethod
    def create_architect_report(cls, request):
        """
        Handles validation and creation of a new ArchitectReport.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ArchitectReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            client = Client.objects.get(user=user)
            reasons = validated_data.pop("reasons")
            with transaction.atomic():
                # Create ArchitectReport instance
                architect_report = ArchitectReport.objects.create(
                    reporting_client=client,
                    reported_architect=validated_data.pop("reported_architect_id"),
                    **validated_data,
                )
                architect_report.reasons.set(reasons)
                architect_report.save()
                return Response(
                    ArchitectReportSerializer(architect_report).data,
                    status=status.HTTP_201_CREATED,
                )
        except IntegrityError as e:
            if "unique constraint" in str(e):
                raise serializers.ValidationError(
                    {"detail": "A report for this architect by this client already exists."}
                )
            raise APIException(detail=f"Error creating architect report: {str(e)}")
        except Client.DoesNotExist:
            raise NotFound(detail="Authenticated user is not a client.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating architect report: {str(e)}")

    @classmethod
    def get_grouped_architect_reports(cls):
        """
        Groups ArchitectReport objects by the architect's email and returns them as a list.

        Returns:
            Response: A response object containing the grouped architect reports.
        """
        queryset = ArchitectReport.objects.all()
        architect_reports = defaultdict(list)

        for report in queryset:
            architect_email = report.reported_architect.user.email
            architect_reports[architect_email].append(ArchitectReportSerializer(report).data)

        # Convert defaultdict to a list of dictionaries for JSON serialization
        grouped_reports = [
            {architect_email: reports} for architect_email, reports in architect_reports.items()
        ]
        return Response(grouped_reports)

    @classmethod
    def get_decisions(cls):
        """
        Retrieve all possible decisions for the corresponding type and return as a serialized
          Response.

        Returns:
            Response: A serialized response containing the list of decisions.
        """
        decisions = Decision.objects.filter(report_type="Architect")
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
        reasons = Reason.objects.filter(report_type="Architect")
        serialized_reasons = ReasonSerializer(reasons, many=True)
        return Response(serialized_reasons.data)

    @classmethod
    def change_architect_report_status(cls, request, pk):
        """
        Change the status of a specific ArchitectReport.

        Args:
            request (Request): The request object containing the status.
            pk (int): The primary key of the ArchitectReport to update.

        Returns:
            Response: A response object containing the updated report or an error message.
        """
        try:
            report = ArchitectReport.objects.get(pk=pk)
            new_status = request.data.get("status")
            if new_status not in dict(STATUS_CHOICES):
                raise serializers.ValidationError(detail="Invalid status choice.")

            report.status = new_status
            report.save()
            return Response(ArchitectReportSerializer(report).data)
        except ArchitectReport.DoesNotExist:
            raise NotFound(detail="ArchitectReport not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating report status: {str(e)}")
