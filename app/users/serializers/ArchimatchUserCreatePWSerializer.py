"""
Module containing ArchimatchUserCreatePWSerializer class.

This module provides a serializer for creating an ArchimatchUser object along with
 setting a password.

Classes:
    ArchimatchUserCreatePWSerializer: Serializer for creating ArchimatchUser with
     password.
"""

from rest_framework import serializers


class ArchimatchUserCreatePWSerializer(serializers.Serializer):
    """
    Serializer for creating ArchimatchUser with password.

    This serializer is used for creating an ArchimatchUser object along with setting
     a password.

    Fields:
        id: The unique identifier of the user.
        password: The password to set for the user. (write-only)
        confirm_password: Confirmation of the password. (write-only)

    Notes:
        - Both `password` and `confirm_password` are write-only fields, meaning they are
         used for input only.
    """

    id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
