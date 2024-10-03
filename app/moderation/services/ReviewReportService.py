"""
Service module for the ReviewReport model.

This module defines the service for handling the business logic and exceptions
related to ReviewReport creation and management.

Classes:
    ReviewReportService: Service class for ReviewReport operations.
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
from app.moderation.models.ReviewReport import ReviewReport
from app.moderation.serializers.DecisionSerializer import DecisionSerializer
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.moderation.serializers.ReviewReportSerializer import ReviewReportSerializer
from app.moderation.services.ReportAction import REVIEW_DECISION_ACTION_MAP
from app.users.models.Architect import Architect


class ReviewReportService:
    """
    Service class for handling ReviewReport operations.

    Handles business logic and exception handling for ReviewReport creation and management.

    Methods:
        create_review_report(request): Handles validation and creation of a new ReviewReport.
    """
    pagination_class = CustomPagination
    
    @classmethod
    def create_review_report(cls, request):
        """
        Handles validation and creation of a new ReviewReport.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ReviewReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            architect = Architect.objects.get(user=user)
            reasons = validated_data.pop("report_reasons")
            with transaction.atomic():
                # Create ReviewReport instance
                review_report = ReviewReport.objects.create(
                    reporting_architect=architect,
                    reported_review=validated_data.pop("reported_review_id"),
                    **validated_data,
                )
                review_report.reasons.set(reasons)
                review_report.save()
                return True,ReviewReportSerializer(review_report).data
 
        except IntegrityError as e:
            if "unique constraint" in str(e):
                raise serializers.ValidationError(
                    {"detail": "A report for this review by this architect already exists."}
                )
            raise APIException(detail=f"Error creating review report: {str(e)}")
        except Architect.DoesNotExist:
            raise NotFound(detail="Authenticated user is not an architect.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating review report: {str(e)}")

    @classmethod
    def get_decisions(cls):
        """
        Retrieve all possible decisions for the corresponding type and return as a serialized
         Response.

        Returns:
            Response: A serialized response containing the list of decisions.
        """
        decisions = Decision.objects.filter(report_type="Review")
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
        reasons = Reason.objects.filter(report_type="Review")
        serialized_reasons = ReasonSerializer(reasons, many=True)
        return True,serialized_reasons.data

    @classmethod
    def change_architect_report_status(cls, request, pk):
        """
        Change the status of a specific ReviewReport.

        Args:
            request (Request): The request object containing the status.
            pk (int): The primary key of the ReviewReport to update.

        Returns:
            Response: A response object containing the updated report or an error message.
        """

        report = ReviewReport.objects.get(pk=pk)
        new_status = request.data.get("status")
        if new_status not in dict(STATUS_CHOICES):
            raise serializers.ValidationError(detail="Invalid status choice.")

        report.status = new_status
        report.save()
        return True,ReviewReportSerializer(report).data
        

    @classmethod
    def execute_decision(cls, request, pk):
        """
        Executes the decision related to the given ReviewReport.

        Parameters:
        - request: The request object containing the decision data.
        - pk: The primary key of the ReviewReport instance.

        Returns:
        - A Response object indicating the result of the operation.
        """

        report = ReviewReport.objects.get(pk=pk)

        decision_id = request.data.get("decision_id")
        if not decision_id:
            raise serializers.ValidationError(detail="Decision Id is required.")

        decision = Decision.objects.get(id=decision_id)

        action = REVIEW_DECISION_ACTION_MAP.get(decision.id)
        if not action:
            raise serializers.ValidationError(detail="No valid action found for the decision.")
        report.status = "Treated"
        report.decision = decision
        report.decision_date = timezone.now()
        report.save()

        action.execute(report.reported_review, request.user.admin)

        return True,ReviewReportSerializer(report).data

    
    @classmethod
    def review_reports_get_all(cls, request):
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

        queryset = ReviewReport.objects.all()

        # Instantiate the paginator
        paginator = cls.pagination_class()

        # Apply pagination to the filtered queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ReviewReportSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ReviewReportSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)