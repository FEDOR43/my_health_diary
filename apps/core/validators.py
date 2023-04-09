from __future__ import annotations

import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneValidator:
    message = _("Введите валидный номер телефона.")
    code = "invalid"

    def __init__(self, message: str = None, code: str = None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value: str, region: str = None):
        try:
            value = value if "+" in value else "+" + value
            value = value.replace("+8", "+7")
            phone = phonenumbers.parse(value, region)
        except phonenumbers.NumberParseException:
            raise ValidationError(self.message, code=self.code)

        if (
            not phonenumbers.is_possible_number(phone)
            or not phonenumbers.is_valid_number(phone)
            or not (
                phonenumbers.is_valid_number_for_region(phone, "RU")
                or phonenumbers.is_valid_number_for_region(phone, "BY")
                or phonenumbers.is_valid_number_for_region(phone, "UA")
                or phonenumbers.is_valid_number_for_region(phone, "KZ")
                or phonenumbers.is_valid_number_for_region(phone, "UZ")
            )
        ):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other: PhoneValidator) -> bool:
        return (
            isinstance(other, PhoneValidator)
            and (self.message == other.message)
            and (self.code == other.code)
        )


validate_phone = PhoneValidator()
