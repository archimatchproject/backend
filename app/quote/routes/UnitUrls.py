"""
exposed URLS for announcement app
viewset : AnnouncementViewSet
"""

from django.urls import path

from app.quote.controllers.UnitViewSet import UnitViewSet


unit_urlpatterns = [
    path(
        "unit/get-all",
        UnitViewSet.as_view({"get": "get_all_units"}),
        name="get-all",
    ),
    path(
        "unit/create",
        UnitViewSet.as_view({"post": "create_unit"}),
        name="create",
    ),
    path(
        "unit/delete/<int:pk>/",
        UnitViewSet.as_view({"delete": "delete_unit"}),
        name="delete",
    ),
]
