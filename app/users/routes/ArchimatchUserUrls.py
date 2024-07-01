from django.urls import path
from app.users.controllers import ArchimatchUserViewSet

archimatch_user_urlpatterns = [
    path("archimatch-user/create-password/", ArchimatchUserViewSet.as_view({'post': 'archimatch_user_create_password'}), name="create-password"),
    path("archimatch-user/reset-password/", ArchimatchUserViewSet.as_view({'post': 'archimatch_user_reset_password'}), name="reset-password"),
]