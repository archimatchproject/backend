"""
exposed URLS for users app
viewset : ArchimatchUserViewSet
"""

from django.urls import path

from app.users.controllers.ArchimatchUserViewSet import ArchimatchUserViewSet


archimatch_user_urlpatterns = [
    path(
        "archimatch-user/create-password/",
        ArchimatchUserViewSet.as_view({"post": "archimatch_user_create_password"}),
        name="create-password",
    ),
    path(
        "archimatch-user/reset-password/",
        ArchimatchUserViewSet.as_view({"post": "archimatch_user_reset_password"}),
        name="reset-password",
    ),
    path(
        "archimatch-user/update-data/",
        ArchimatchUserViewSet.as_view({"put": "archimatch_user_update_data"}),
        name="update-data",
    ),
    path(
        "archimatch-user/get-user-data",
        ArchimatchUserViewSet.as_view({"get": "archimatch_user_get_user_data"}),
        name="get-user-data",
    ),
    path(
        "archimatch-user/send-code/",
        ArchimatchUserViewSet.as_view({"post": "send_verification_code"}),
        name="send-code",
    ),
    path(
        "archimatch-user/verify-code/",
        ArchimatchUserViewSet.as_view({"post": "verify_verification_code"}),
        name="verify-code",
    ),
]
