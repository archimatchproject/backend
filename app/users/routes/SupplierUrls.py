"""
exposed URLS for users app
viewset : SupplierViewSet
"""

from django.urls import path

from app.users.controllers.SupplierViewSet import SupplierViewSet


supplier_urlpatterns = [
    path(
        "supplier/signup/",
        SupplierViewSet.as_view({"post": "supplier_signup"}),
        name="signup",
    ),
    path(
        "supplier/login/",
        SupplierViewSet.as_view({"post": "supplier_login"}),
        name="login",
    ),
    path(
        "supplier/first-connection/",
        SupplierViewSet.as_view({"post": "supplier_first_cnx"}),
        name="first-connection",
    ),
    path(
        "supplier/update-profile/",
        SupplierViewSet.as_view({"put": "supplier_update_profile"}),
        name="update-profile",
    ),
    path(
        "supplier/update-bio/",
        SupplierViewSet.as_view({"put": "supplier_update_bio"}),
        name="update-bio",
    ),
    path(
        "supplier/update-presentation-video/",
        SupplierViewSet.as_view({"put": "supplier_update_presentation_video"}),
        name="update-presentation-video",
    ),
    path(
        "supplier/update-links/",
        SupplierViewSet.as_view({"put": "supplier_update_links"}),
        name="update-links",
    ),
    path(
        "supplier/speciality-types/",
        SupplierViewSet.as_view({"get": "get_speciality_types"}),
        name="speciality-types",
    ),
    path(
        "supplier/appearances/",
        SupplierViewSet.as_view({"get": "get_appearances"}),
        name="appearances",
    ),
    path(
        "supplier/get-profile/",
        SupplierViewSet.as_view({"get": "supplier_get_profile"}),
        name="profile",
    ),
    path(
        "supplier/send-reset-password-link/",
        SupplierViewSet.as_view({"post": "supplier_send_reset_password_link"}),
        name="send-reset-password-link",
    ),
    path(
        "supplier/update-profile-image/",
        SupplierViewSet.as_view({"put": "supplier_update_profile_image"}),
        name="update-profile-image",
    ),
    path(
        "supplier/update-cover-image/",
        SupplierViewSet.as_view({"put": "supplier_update_cover_image"}),
        name="update-cover-image",
    ),
    path(
        "supplier/update-visibility/",
        SupplierViewSet.as_view({"put": "supplier_update_visibility"}),
        name="update-visibility",
    ),
    path(
        "supplier/validate-password-token/",
        SupplierViewSet.as_view({"post": "supplier_validate_password_token"}),
        name="validate-password-token",
    ),
    path(
        "supplier/get-all/",
        SupplierViewSet.as_view({"get": "get"}),
        name="get-all",
    ),
    path(
        "supplier/resend-email/<int:pk>/",
        SupplierViewSet.as_view({"post": "supplier_resend_email"}),
        name="resend-email",
    ),
    path(
        "suppliers/delete/<int:pk>/",
        SupplierViewSet.as_view({"delete": "delete"}),
        name="delete-supplier",
    ),
]
