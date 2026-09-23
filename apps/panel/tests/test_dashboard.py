import pytest
from django.urls import reverse

from apps.contact.tests.factories import make_message
from apps.content.tests.factories import make_project

pytestmark = pytest.mark.django_db


def test_dashboard__shows_message_and_project_counts(staff_client):
    make_message(is_read=False)
    make_project(slug="a", is_published=True)
    make_project(slug="b", is_published=False)

    response = staff_client.get(reverse("panel:dashboard"))

    content = response.content.decode()
    assert ">1<" in content
    assert "1 ta o'qilmagan" in content
    assert "1 tasi saytda" in content


def test_dashboard__no_unread__shows_all_read_hint(staff_client):
    make_message(is_read=True)

    response = staff_client.get(reverse("panel:dashboard"))

    assert b"Hammasi o'qilgan" in response.content
