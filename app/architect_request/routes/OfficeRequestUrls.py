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
    )
]
