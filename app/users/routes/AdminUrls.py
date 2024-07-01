"""
exposed URLS for users app
viewset : AdminViewSet
"""

from django.urls import path

from app.users.controllers import AdminViewSet


admin_urlpatterns = [
    path("admin/create/", AdminViewSet.as_view({"post": "create"}), name="admin-create"),
    path(
        "admin/update/<int:pk>/",
        AdminViewSet.as_view({"put": "update"}),
        name="admin-update",
    ),
]
