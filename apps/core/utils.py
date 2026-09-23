import hashlib
import hmac

from django.conf import settings
from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    real_ip = request.META.get("HTTP_X_REAL_IP")
    if real_ip:
        return real_ip
    return request.META.get("REMOTE_ADDR", "")


def hash_ip(ip: str) -> str:
    return hmac.new(settings.IP_HASH_SALT.encode(), ip.encode(), hashlib.sha256).hexdigest()
