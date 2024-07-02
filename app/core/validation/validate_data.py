"""
Module for defining Validation methods

"""

import re

from app.core.validation.exceptions import InvalidPhoneNumberException


def is_valid_phone_number(phone_number, region="TN"):
    """
    is_valid_phone_number

    Args:
        phone_number
        region  Defaults to 'TN'.

    Raises:
        InvalidPhoneNumberException

    Tunisian phone numbers are expected to be in the format +216XXXXXXXX
    """
    if region == "TN":

        pattern = r"^\+216\d{8}$"
        if re.match(pattern, phone_number) is None:
            raise InvalidPhoneNumberException("Invalid phone number format for region TN")
    else:
        raise InvalidPhoneNumberException("Unsupported region")
    return True
