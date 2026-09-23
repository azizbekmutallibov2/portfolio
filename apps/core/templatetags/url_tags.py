from urllib.parse import urlparse

from django import template

register = template.Library()


@register.filter
def display_url(value: str) -> str:
    if not value:
        return ""
    parsed = urlparse(value)
    host = parsed.netloc or parsed.path
    if host.startswith("www."):
        host = host[4:]
    path = parsed.path.rstrip("/") if parsed.netloc else ""
    return (host + path).rstrip("/")
