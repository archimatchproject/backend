"""
Exposed URLs for the OfficeReportArchitect app.

This module defines the URL patterns for the OfficeReportArchitectViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.moderation.controllers.OfficeReportArchitectViewSet import OfficeReportArchitectViewSet


office_report_urlpatterns = [
    path(
        "office-report",
        OfficeReportArchitectViewSet.as_view({"get": "list"}),
        name="office-report-list",
    ),
    path(
        "office-report/create/",
        OfficeReportArchitectViewSet.as_view({"post": "create"}),
        name="office-report-create",
    ),
    path(
        "office-report/<int:pk>",
        OfficeReportArchitectViewSet.as_view({"get": "retrieve"}),
        name="office-report-retrieve",
    ),
    path(
        "office-report/update/<int:pk>/",
        OfficeReportArchitectViewSet.as_view({"put": "update"}),
        name="office-report-update",
    ),
    path(
        "office-report/delete/<int:pk>/",
        OfficeReportArchitectViewSet.as_view({"delete": "destroy"}),
        name="office-report-delete",
    ),
    path(
        "office-report/decisions",
        OfficeReportArchitectViewSet.as_view({"get": "get_decisions"}),
        name="office-report-decisions",
    ),
    path(
        "office-report/reasons",
        OfficeReportArchitectViewSet.as_view({"get": "get_reasons"}),
        name="office-report-reasons",
    ),
    path(
        "office-report/<int:pk>/change-status/",
        OfficeReportArchitectViewSet.as_view({"post": "change_status"}),
        name="office-report-change-status",
    ),
    path(
        "office-report/execute-decision/",
        OfficeReportArchitectViewSet.as_view({"post": "execute_decision"}),
        name="office-report-execute-decision",
    ),
]
