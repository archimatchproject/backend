"""
Exposed URLs for the ReviewReport app.

This module defines the URL patterns for the ReviewReportViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.moderation.controllers.ReviewReportViewSet import ReviewReportViewSet


review_report_urlpatterns = [
    path(
        "review-report",
        ReviewReportViewSet.as_view({"get": "list"}),
        name="review-report-list",
    ),
    path(
        "review-report/create/",
        ReviewReportViewSet.as_view({"post": "create"}),
        name="review-report-create",
    ),
    path(
        "review-report/<int:pk>",
        ReviewReportViewSet.as_view({"get": "retrieve"}),
        name="review-report-retrieve",
    ),
    path(
        "review-report/update/<int:pk>/",
        ReviewReportViewSet.as_view({"put": "update"}),
        name="review-report-update",
    ),
    path(
        "review-report/delete/<int:pk>/",
        ReviewReportViewSet.as_view({"delete": "destroy"}),
        name="review-report-delete",
    ),
    path(
        "review-report/decisions",
        ReviewReportViewSet.as_view({"get": "get_decisions"}),
        name="review-report-decisions",
    ),
    path(
        "review-report/reasons",
        ReviewReportViewSet.as_view({"get": "get_reasons"}),
        name="review-report-reasons",
    ),
    path(
        "review-report/<int:pk>/change-status/",
        ReviewReportViewSet.as_view({"post": "change_status"}),
        name="review-report-change-status",
    ),
    path(
        "review-report/<int:pk>/execute-decision/",
        ReviewReportViewSet.as_view({"post": "execute_decision"}),
        name="review-report-execute-decision",
    ),
]
