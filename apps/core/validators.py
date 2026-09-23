import re

from django.core.exceptions import ValidationError

_ALLOWED_CHARS_RE = re.compile(r"^[0-9+()\-\s]+$")
_DIGITS_RE = re.compile(r"\D")

PHONE_ERROR = "Telefon raqam noto'g'ri."


def validate_phone(value: str) -> None:
    if not value or not _ALLOWED_CHARS_RE.fullmatch(value):
        raise ValidationError(PHONE_ERROR)
    digits = _DIGITS_RE.sub("", value)
    if not (7 <= len(digits) <= 15):
        raise ValidationError(PHONE_ERROR)
