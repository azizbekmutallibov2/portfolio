from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from apps.core.validators import validate_phone

_email_validator = EmailValidator()

CONTACT_ERROR = "Telefon raqam yoki email kiriting."


def validate_contact(value: str) -> None:
    value = value.strip()
    try:
        _email_validator(value)
        return
    except ValidationError:
        pass
    try:
        validate_phone(value)
    except ValidationError:
        raise ValidationError(CONTACT_ERROR, code="invalid_contact") from None
