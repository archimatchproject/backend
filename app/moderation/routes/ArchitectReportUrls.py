"""
Exposed URLs for the ArchitectReport app.

This module defines the URL patterns for the ArchitectReportViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.moderation.controllers.ArchitectReportViewSet import ArchitectReportViewSet


architect_report_urlpatterns = [
    path(
        "architect-report",
        ArchitectReportViewSet.as_view({"get": "list"}),
        name="architect-report-list",
    ),
    path(
        "architect-report/create/",
        ArchitectReportViewSet.as_view({"post": "create"}),
        name="architect-report-create",
    ),
    path(
        "architect-report/<int:pk>",
        ArchitectReportViewSet.as_view({"get": "retrieve"}),
        name="architect-report-retrieve",
    ),
    path(
        "architect-report/update/<int:pk>/",
        ArchitectReportViewSet.as_view({"put": "update"}),
        name="architect-report-update",
    ),
    path(
        "architect-report/delete/<int:pk>/",
        ArchitectReportViewSet.as_view({"delete": "destroy"}),
        name="architect-report-delete",
    ),
    path(
        "architect-report/decisions",
        ArchitectReportViewSet.as_view({"get": "get_decisions"}),
        name="architect-report-decisions",
    ),
    path(
        "architect-report/reasons",
        ArchitectReportViewSet.as_view({"get": "get_reasons"}),
        name="architect-report-reasons",
    ),
]
