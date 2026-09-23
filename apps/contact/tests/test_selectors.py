from datetime import timedelta

import pytest
from django.utils import timezone

from apps.contact.models import ContactMessage
from apps.contact.selectors import message_counts, message_get, message_recent_count
from apps.contact.tests.factories import make_message

pytestmark = pytest.mark.django_db


def test_message_get__missing__returns_none():
    assert message_get(pk=999) is None


def test_message_counts__single_query(django_assert_num_queries):
    make_message(is_read=True)
    make_message(is_read=False)

    with django_assert_num_queries(1):
        counts = message_counts()

    assert counts == {"total": 2, "unread": 1}


def test_message_recent_count__within_window__counted():
    message = make_message(ip_hash="abc123")

    since = timezone.now() - timedelta(hours=1)

    assert message_recent_count(ip_hash="abc123", since=since) == 1
    assert message.pk is not None


def test_message_recent_count__outside_window__not_counted():
    message = make_message(ip_hash="abc123")
    ContactMessage.objects.filter(pk=message.pk).update(
        created_at=timezone.now() - timedelta(hours=2)
    )

    since = timezone.now() - timedelta(hours=1)

    assert message_recent_count(ip_hash="abc123", since=since) == 0


def test_message_recent_count__different_ip__not_counted():
    make_message(ip_hash="abc123")

    since = timezone.now() - timedelta(hours=1)

    assert message_recent_count(ip_hash="different", since=since) == 0
