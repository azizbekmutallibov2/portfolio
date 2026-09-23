from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.contact.exceptions import RateLimitExceeded
from apps.contact.models import ContactMessage
from apps.contact.selectors import message_recent_count
from apps.core.utils import hash_ip

RATE_LIMIT_MESSAGE = "Juda ko'p xabar yuborildi. Bir soatdan keyin qayta urinib ko'ring."


@transaction.atomic
def message_create(
    *, name: str, contact: str, body: str, ip: str, user_agent: str = ""
) -> ContactMessage:
    ip_hash = hash_ip(ip) if ip else ""
    if ip_hash:
        since = timezone.now() - timedelta(hours=1)
        recent = message_recent_count(ip_hash=ip_hash, since=since)
        if recent >= settings.CONTACT_RATE_LIMIT_PER_HOUR:
            raise RateLimitExceeded(RATE_LIMIT_MESSAGE)

    message = ContactMessage(
        name=name.strip(),
        contact=contact.strip(),
        body=body.strip(),
        ip_hash=ip_hash,
        user_agent=user_agent[:300],
    )
    message.full_clean()
    message.save()
    return message


def message_mark_read(*, message: ContactMessage) -> ContactMessage:
    if not message.is_read:
        message.is_read = True
        message.save(update_fields=["is_read", "updated_at"])
    return message


def message_delete(*, message: ContactMessage) -> None:
    message.delete()
