import pytest
from django.test import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_dashboard__anonymous__redirects_to_login():
    client = Client()

    response = client.get(reverse("panel:dashboard"))

    assert response.status_code == 302
    assert reverse("panel:login") in response.url


def test_dashboard__regular_user__forbidden(regular_user):
    client = Client()
    client.force_login(regular_user)

    response = client.get(reverse("panel:dashboard"))

    assert response.status_code == 403


def test_dashboard__staff_user__200(staff_client):
    response = staff_client.get(reverse("panel:dashboard"))

    assert response.status_code == 200


def test_login__valid_staff_credentials__redirects_to_dashboard(staff_user):
    client = Client()

    response = client.post(reverse("panel:login"), {"username": "staff", "password": "password123"})

    assert response.status_code == 302
    assert response.url == reverse("panel:dashboard")


def test_login__wrong_password__shows_generic_error(staff_user):
    client = Client()

    response = client.post(
        reverse("panel:login"), {"username": "staff", "password": "wrong-password"}
    )

    assert response.status_code == 200
    assert b"Login yoki parol noto" in response.content


def test_login__non_staff_user__shows_generic_error(regular_user):
    client = Client()

    response = client.post(
        reverse("panel:login"), {"username": "regular", "password": "password123"}
    )

    assert response.status_code == 200
    assert b"Login yoki parol noto" in response.content


def test_login__panel_page__has_noindex_meta(staff_user):
    client = Client()

    response = client.get(reverse("panel:login"))

    assert b'name="robots" content="noindex, nofollow"' in response.content


def test_logout__get__not_allowed(staff_client):
    response = staff_client.get(reverse("panel:logout"))

    assert response.status_code == 405


def test_logout__post__logs_out_and_redirects(staff_client):
    response = staff_client.post(reverse("panel:logout"))

    assert response.status_code == 302

    protected = staff_client.get(reverse("panel:dashboard"))
    assert protected.status_code == 302
