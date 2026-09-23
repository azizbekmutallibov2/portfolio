import pytest

from apps.contact.tests.factories import make_message

pytestmark = pytest.mark.django_db


def test_contact_message__str__includes_name():
    message = make_message(name="Aziz Karimov")

    assert "Aziz Karimov" in str(message)
