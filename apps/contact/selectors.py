from datetime import datetime

from django.db.models import Count, Q, QuerySet

from apps.contact.models import ContactMessage


def message_list() -> QuerySet[ContactMessage]:
    return ContactMessage.objects.all()


def message_get(*, pk: int) -> ContactMessage | None:
    return ContactMessage.objects.filter(pk=pk).first()


def message_counts() -> dict:
    return ContactMessage.objects.aggregate(
        total=Count("id"),
        unread=Count("id", filter=Q(is_read=False)),
    )


def message_recent_count(*, ip_hash: str, since: datetime) -> int:
    return ContactMessage.objects.filter(ip_hash=ip_hash, created_at__gte=since).count()
