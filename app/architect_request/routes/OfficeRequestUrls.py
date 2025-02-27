"""
exposed URLS for office request app
viewset : OfficeRequestViewSet
"""

from django.urls import path

from app.architect_request.controllers.OfficeRequestViewSet import OfficeRequestViewSet


office_request_urlpatterns = [
    path(
        "create-office-request/",
        OfficeRequestViewSet.as_view({"post": "create_office_request"}),
        name="create-office-request",
    ),
    path(
        "get-office-requests",
        OfficeRequestViewSet.as_view({"get": "get"}),
        name="office-requests-list",
    ),
    path(
        "office-admin-refuse/<int:pk>/",
        OfficeRequestViewSet.as_view({"post": "office_admin_refuse"}),
        name="office-request-admin-refuse",
    ),
    path(
        "office-admin-accept/<int:pk>/",
        OfficeRequestViewSet.as_view({"post": "office_admin_accept"}),
        name="office-request-admin-accept",
    ),
    path(
        "office-add-note/<int:pk>/",
        OfficeRequestViewSet.as_view({"post": "office_add_note"}),
        name="add-note-to-office-request",
    ),
    path(
        "office-reschedule-meeting/<int:pk>/",
        OfficeRequestViewSet.as_view({"put": "reschedule"}),
        name="reschedule",
    ),
    path(
        "admin-assign-office-responsable/<int:pk>/",
        OfficeRequestViewSet.as_view({"post": "admin_assign_office_responsable"}),
        name="office-request-admin-assign-responsable",
    ),
]
