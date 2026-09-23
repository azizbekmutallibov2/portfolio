from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def _error(domain: str) -> ValidationError:
    return ValidationError(f"Havola {domain} manziliga olib borishi kerak.")


def validate_github_url(value: str) -> None:
    parsed = urlparse(value)
    if parsed.netloc.lower() not in {"github.com", "www.github.com"} or not parsed.path.strip("/"):
        raise _error("github.com")


def validate_telegram_url(value: str) -> None:
    parsed = urlparse(value)
    if parsed.netloc.lower() != "t.me":
        raise _error("t.me")


def validate_linkedin_url(value: str) -> None:
    parsed = urlparse(value)
    valid_host = parsed.netloc.lower() in {"linkedin.com", "www.linkedin.com"}
    if not valid_host or not parsed.path.startswith("/in/"):
        raise _error("linkedin.com")
