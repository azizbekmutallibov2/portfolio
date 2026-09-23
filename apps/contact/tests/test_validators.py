import pytest
from django.core.exceptions import ValidationError

from apps.contact.validators import validate_contact


@pytest.mark.parametrize("value", ["test@example.com", "+998901234567", "998901234567"])
def test_validate_contact__valid_values(value):
    validate_contact(value)


@pytest.mark.parametrize("value", ["", "abc", "not-an-email-or-phone"])
def test_validate_contact__invalid_values__raise(value):
    with pytest.raises(ValidationError):
        validate_contact(value)
