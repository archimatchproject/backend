from rest_framework.exceptions import APIException
from rest_framework import status


class UserDataException(APIException):
    def __init__(self, detail=None, status_code=None):
        self.detail = detail or self.default_detail
        self.status_code = status_code or self.default_status_code

    default_detail = 'A custom API exception occurred.'
    default_status_code = status.HTTP_400_BAD_REQUEST