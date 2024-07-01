from django.urls import path
from app.architect_request.controllers.ArchitectRequestViewSet import ArchitectRequestViewSet

architect_request_urlpatterns = [
    path("create-architect-request/", ArchitectRequestViewSet.as_view({'post': 'create_architect_request'}), name="create-architect-request"),
]
