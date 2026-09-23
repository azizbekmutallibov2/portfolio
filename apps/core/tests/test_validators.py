import pytest
from django.core.exceptions import ValidationError

from apps.core.validators import validate_phone


@pytest.mark.parametrize(
    "value",
    ["+998901234567", "998901234567", "(90) 123-45-67", "+1 555 123 4567"],
)
def test_validate_phone__valid_values__pass(value):
    validate_phone(value)


@pytest.mark.parametrize("value", ["", "abc", "123", "+998" + "1" * 20])
def test_validate_phone__invalid_values__raise(value):
    with pytest.raises(ValidationError):
        validate_phone(value)
