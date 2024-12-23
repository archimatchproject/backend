"""
Exposed URLs for the SelectionReport app.

This module defines the URL patterns for the SelectionReportViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.moderation.controllers.SelectionReportViewSet import SelectionReportViewSet


selection_report_urlpatterns = [
    path(
        "selection-report",
        SelectionReportViewSet.as_view({"get": "list"}),
        name="selection-report-list",
    ),
    path(
        "selection-report/create/",
        SelectionReportViewSet.as_view({"post": "create"}),
        name="selection-report-create",
    ),
    path(
        "selection-report/<int:pk>",
        SelectionReportViewSet.as_view({"get": "retrieve"}),
        name="selection-report-retrieve",
    ),
    path(
        "selection-report/update/<int:pk>/",
        SelectionReportViewSet.as_view({"put": "update"}),
        name="selection-report-update",
    ),
    path(
        "selection-report/delete/<int:pk>/",
        SelectionReportViewSet.as_view({"delete": "destroy"}),
        name="selection-report-delete",
    ),
    path(
        "selection-report/decisions",
        SelectionReportViewSet.as_view({"get": "get_decisions"}),
        name="selection-report-decisions",
    ),
    path(
        "selection-report/reasons",
        SelectionReportViewSet.as_view({"get": "get_reasons"}),
        name="selection-report-reasons",
    ),
    path(
        "selection-report/<int:pk>/change-status/",
        SelectionReportViewSet.as_view({"post": "change_status"}),
        name="selection-report-change-status",
    ),
    path(
        "selection-report/execute-decision/",
        SelectionReportViewSet.as_view({"post": "execute_decision"}),
        name="selection-report-execute-decision",
    ),
]
