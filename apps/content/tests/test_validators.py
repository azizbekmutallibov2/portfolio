import pytest
from django.core.exceptions import ValidationError

from apps.content.validators import (
    validate_github_url,
    validate_linkedin_url,
    validate_telegram_url,
)


@pytest.mark.parametrize(
    "value",
    ["https://github.com/azizillo", "https://www.github.com/azizillo"],
)
def test_validate_github_url__valid(value):
    validate_github_url(value)


@pytest.mark.parametrize(
    "value",
    ["https://github.com/", "https://gitlab.com/azizillo", "https://github.com"],
)
def test_validate_github_url__invalid(value):
    with pytest.raises(ValidationError):
        validate_github_url(value)


def test_validate_telegram_url__valid():
    validate_telegram_url("https://t.me/azizillo")


def test_validate_telegram_url__invalid_host():
    with pytest.raises(ValidationError):
        validate_telegram_url("https://telegram.me/azizillo")


@pytest.mark.parametrize(
    "value",
    ["https://linkedin.com/in/azizillo", "https://www.linkedin.com/in/azizillo"],
)
def test_validate_linkedin_url__valid(value):
    validate_linkedin_url(value)


@pytest.mark.parametrize(
    "value",
    ["https://linkedin.com/azizillo", "https://linkedin.com/company/x"],
)
def test_validate_linkedin_url__invalid_path(value):
    with pytest.raises(ValidationError):
        validate_linkedin_url(value)
