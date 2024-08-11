"""
Exposed URLs for the ProjectReport app.

This module defines the URL patterns for the ProjectReportViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.moderation.controllers.ProjectReportViewSet import ProjectReportViewSet


project_report_urlpatterns = [
    path(
        "project-report",
        ProjectReportViewSet.as_view({"get": "list"}),
        name="project-report-list",
    ),
    path(
        "project-report/create/",
        ProjectReportViewSet.as_view({"post": "create"}),
        name="project-report-create",
    ),
    path(
        "project-report/<int:pk>",
        ProjectReportViewSet.as_view({"get": "retrieve"}),
        name="project-report-retrieve",
    ),
    path(
        "project-report/update/<int:pk>/",
        ProjectReportViewSet.as_view({"put": "update"}),
        name="project-report-update",
    ),
    path(
        "project-report/delete/<int:pk>/",
        ProjectReportViewSet.as_view({"delete": "destroy"}),
        name="project-report-delete",
    ),
    path(
        "project-report/decisions",
        ProjectReportViewSet.as_view({"get": "get_decisions"}),
        name="project-report-decisions",
    ),
    path(
        "project-report/reasons",
        ProjectReportViewSet.as_view({"get": "get_reasons"}),
        name="project-report-reasons",
    ),
    path(
        "project-report/<int:pk>/change-status/",
        ProjectReportViewSet.as_view({"post": "change_status"}),
        name="project-report-change-status",
    ),
    path(
        "project-report/<int:pk>/execute-decision/",
        ProjectReportViewSet.as_view({"post": "execute_decision"}),
        name="project-report-execute-decision",
    ),
]
