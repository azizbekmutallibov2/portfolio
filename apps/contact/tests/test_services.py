import pytest
from django.core.exceptions import ValidationError
from django.test import override_settings

from apps.contact.exceptions import RateLimitExceeded
from apps.contact.services import message_create, message_delete, message_mark_read
from apps.contact.tests.factories import make_message
from apps.core.utils import hash_ip

pytestmark = pytest.mark.django_db


def test_message_create__valid_data__saves_and_hashes_ip():
    message = message_create(
        name="  Aziz  ",
        contact="test@example.com",
        body="Salom, bu test xabari.",
        ip="203.0.113.5",
    )

    assert message.name == "Aziz"
    assert message.ip_hash == hash_ip("203.0.113.5")
    assert message.ip_hash != "203.0.113.5"


def test_message_create__no_ip__skips_rate_limit_and_hash():
    message = message_create(
        name="Aziz", contact="test@example.com", body="Salom, bu test xabari.", ip=""
    )

    assert message.ip_hash == ""


def test_message_create__invalid_contact__raises_validation_error():
    with pytest.raises(ValidationError):
        message_create(
            name="Aziz", contact="not-valid", body="Salom, bu test xabari.", ip="203.0.113.5"
        )


@override_settings(CONTACT_RATE_LIMIT_PER_HOUR=2)
def test_message_create__over_limit__raises_rate_limit():
    ip = "203.0.113.9"
    message_create(name="Aziz", contact="a@example.com", body="Birinchi xabar matni.", ip=ip)
    message_create(name="Vali", contact="b@example.com", body="Ikkinchi xabar matni.", ip=ip)

    with pytest.raises(RateLimitExceeded):
        message_create(name="Olim", contact="c@example.com", body="Uchinchi xabar matni.", ip=ip)


def test_message_create__user_agent_truncated_to_300_chars():
    message = message_create(
        name="Aziz",
        contact="test@example.com",
        body="Salom, bu test xabari.",
        ip="203.0.113.5",
        user_agent="x" * 400,
    )

    assert len(message.user_agent) == 300


def test_message_mark_read__unread__marks_as_read():
    message = make_message(is_read=False)

    updated = message_mark_read(message=message)

    assert updated.is_read is True


def test_message_mark_read__already_read__idempotent():
    message = make_message(is_read=True)

    updated = message_mark_read(message=message)

    assert updated.is_read is True


def test_message_delete__removes_message():
    message = make_message()
    pk = message.pk

    message_delete(message=message)

    from apps.contact.models import ContactMessage

    assert not ContactMessage.objects.filter(pk=pk).exists()
