"""
exposed URLS for users app
viewset : AdminViewSet
"""

from django.urls import path

from app.users.controllers.AdminViewSet import AdminViewSet


admin_urlpatterns = [
    path(
        "admin/create/",
        AdminViewSet.as_view({"post": "create"}),
        name="admin-create",
    ),
    path(
        "admin/update/<int:pk>/",
        AdminViewSet.as_view({"put": "update"}),
        name="admin-update",
    ),
    path(
        "admin/get-admins",
        AdminViewSet.as_view({"get": "list"}),
        name="admin-list",
    ),
    path(
        "admin/get-permissions",
        AdminViewSet.as_view({"get": "get_admin_permissions"}),
        name="admin-get-permissions",
    ),
    path(
        "admin/delete/<int:pk>/",
        AdminViewSet.as_view({"delete": "destroy"}),
        name="admin-delete",
    ),
]
