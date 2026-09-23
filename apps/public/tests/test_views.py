import pytest
from django.test import Client
from django.urls import reverse

from apps.contact.models import ContactMessage
from apps.content.services import site_settings_update
from apps.content.tests.factories import make_project

pytestmark = pytest.mark.django_db


@pytest.fixture
def client() -> Client:
    return Client()


def test_home__returns_200_with_all_section_ids(client):
    response = client.get(reverse("public:home"))

    assert response.status_code == 200
    content = response.content.decode()
    for section_id in ["projects", "stack", "infra", "education", "contact"]:
        assert f'id="{section_id}"' in content


def test_home__query_count(client, django_assert_max_num_queries):
    make_project(slug="a")

    with django_assert_max_num_queries(2):
        client.get(reverse("public:home"))


def test_home__unpublished_project__not_shown(client):
    make_project(slug="hidden", title="Hidden Project", is_published=False)

    response = client.get(reverse("public:home"))

    assert b"Hidden Project" not in response.content


def test_home__no_projects__shows_empty_state(client):
    response = client.get(reverse("public:home"))

    assert b"Loyihalar tez orada qo'shiladi." in response.content


def test_home__empty_profile_links__section_not_rendered(client):
    response = client.get(reverse("public:home"))

    assert b'id="profiles"' not in response.content


def test_home__profile_links_present__section_rendered(client):
    site_settings_update(data={"github_url": "https://github.com/azizillo"}, fields=["github_url"])

    response = client.get(reverse("public:home"))

    assert b'id="profiles"' in response.content
    assert b"github.com/azizillo" in response.content


def test_contact_get__returns_405(client):
    response = client.get(reverse("public:contact"))

    assert response.status_code == 405


def test_contact_post__valid_data__redirects_and_saves(client):
    response = client.post(
        reverse("public:contact"),
        {
            "name": "Aziz",
            "contact": "test@example.com",
            "message": "Salom, bu test xabari matni.",
            "website": "",
        },
    )

    assert response.status_code == 302
    assert ContactMessage.objects.count() == 1


def test_contact_post__invalid_data__does_not_save_and_shows_errors(client):
    response = client.post(
        reverse("public:contact"),
        {"name": "A", "contact": "not-valid", "message": "short", "website": ""},
    )

    assert response.status_code == 200
    assert ContactMessage.objects.count() == 0
    assert b"Ism kamida 2 ta harf" in response.content


def test_contact_post__honeypot_filled__redirects_without_saving(client):
    response = client.post(
        reverse("public:contact"),
        {
            "name": "Aziz",
            "contact": "test@example.com",
            "message": "Salom, bu test xabari matni.",
            "website": "http://spam.example.com",
        },
    )

    assert response.status_code == 302
    assert ContactMessage.objects.count() == 0


def test_contact_post__over_rate_limit__returns_429(client, settings):
    settings.CONTACT_RATE_LIMIT_PER_HOUR = 1
    payload = {
        "name": "Aziz",
        "contact": "test@example.com",
        "message": "Salom, bu test xabari matni.",
        "website": "",
    }

    client.post(reverse("public:contact"), payload)
    response = client.post(reverse("public:contact"), payload)

    assert response.status_code == 429


def test_robots__disallows_panel_and_api(client):
    response = client.get(reverse("public:robots"))

    content = response.content.decode()
    assert "Disallow: /panel/" in content
    assert "Disallow: /api/" in content


def test_sitemap__returns_200(client):
    response = client.get("/sitemap.xml")

    assert response.status_code == 200
