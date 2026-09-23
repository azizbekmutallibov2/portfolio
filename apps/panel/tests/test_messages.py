import pytest
from django.urls import reverse

from apps.contact.models import ContactMessage
from apps.contact.tests.factories import make_message

pytestmark = pytest.mark.django_db


def test_messages_list__anonymous__redirects_to_login():
    from django.test import Client

    response = Client().get(reverse("panel:messages"))

    assert response.status_code == 302


def test_messages_list__shows_messages(staff_client):
    make_message(name="Birinchi Xabar")

    response = staff_client.get(reverse("panel:messages"))

    assert response.status_code == 200
    assert b"Birinchi Xabar" in response.content


def test_messages_list__empty__shows_empty_state(staff_client):
    response = staff_client.get(reverse("panel:messages"))

    assert b"Hali xabar yo'q." in response.content


def test_messages_list__pagination(staff_client):
    for i in range(25):
        make_message(name=f"Xabar {i}", contact=f"user{i}@example.com")

    response = staff_client.get(reverse("panel:messages"))

    assert b"1 / 2" in response.content


def test_message_detail__marks_as_read(staff_client):
    message = make_message(is_read=False)

    response = staff_client.get(reverse("panel:message-detail", args=[message.pk]))

    assert response.status_code == 200
    message.refresh_from_db()
    assert message.is_read is True


def test_message_detail__missing__404(staff_client):
    response = staff_client.get(reverse("panel:message-detail", args=[999]))

    assert response.status_code == 404


def test_message_delete__removes_and_redirects(staff_client):
    message = make_message()

    response = staff_client.post(reverse("panel:message-delete", args=[message.pk]))

    assert response.status_code == 302
    assert not ContactMessage.objects.filter(pk=message.pk).exists()


def test_message_delete__get__not_allowed(staff_client):
    message = make_message()

    response = staff_client.get(reverse("panel:message-delete", args=[message.pk]))

    assert response.status_code == 405


def test_message_delete__missing__404(staff_client):
    response = staff_client.post(reverse("panel:message-delete", args=[999]))

    assert response.status_code == 404
