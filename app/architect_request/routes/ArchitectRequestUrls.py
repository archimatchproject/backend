"""
exposed URLS for architect request app
viewset : ArchitectRequestViewSet
"""

from django.urls import path

from app.architect_request.controllers.ArchitectRequestViewSet import ArchitectRequestViewSet


architect_request_urlpatterns = [
    path(
        "create-architect-request/",
        ArchitectRequestViewSet.as_view({"post": "create_architect_request"}),
        name="create-architect-request",
    ),
    path(
        "get-architect-requests",
        ArchitectRequestViewSet.as_view({"get": "get"}),
        name="architect-requests-list",
    ),
    path(
        "retrieve/<int:pk>",
        ArchitectRequestViewSet.as_view({"get": "retrieve"}),
        name="architect-request-retrieve",
    ),
    path(
        "update/<int:pk>/",
        ArchitectRequestViewSet.as_view({"put": "update"}),
        name="architect-request-update",
    ),
    path(
        "delete/<int:pk>/",
        ArchitectRequestViewSet.as_view({"delete": "destroy"}),
        name="architect-request-destroy",
    ),
    path(
        "admin-accept/<int:pk>/",
        ArchitectRequestViewSet.as_view({"post": "admin_accept"}),
        name="architect-request-admin-accept",
    ),
    path(
        "admin-refuse/<int:pk>/",
        ArchitectRequestViewSet.as_view({"post": "admin_refuse"}),
        name="architect-request-admin-refuse",
    ),
    path(
        "admin-assign-responsable/<int:pk>/",
        ArchitectRequestViewSet.as_view({"post": "admin_assign_responsable"}),
        name="architect-request-admin-assign-responsable",
    ),
    path(
        "add-note/<int:pk>/",
        ArchitectRequestViewSet.as_view({"post": "add_note"}),
        name="architect-request-add-note",
    ),
    path(
        "project-categories",
        ArchitectRequestViewSet.as_view({"get": "get_project_categories"}),
        name="project-categories",
    ),
    path(
        "property-types",
        ArchitectRequestViewSet.as_view({"get": "get_property_types"}),
        name="property-types",
    ),
    path(
        "work-types",
        ArchitectRequestViewSet.as_view({"get": "get_work_types"}),
        name="work-types",
    ),
    path(
        "architectural-styles",
        ArchitectRequestViewSet.as_view({"get": "get_architectural_styles"}),
        name="architectural-styles",
    ),
    path(
        "reschedule-meeting/<int:pk>/",
        ArchitectRequestViewSet.as_view({"put": "reschedule"}),
        name="reschedule",
    ),
    path(
        "time-slots",
        ArchitectRequestViewSet.as_view({"get": "get_time_slots"}),
        name="architect-request-time-slots",
    ),
]
