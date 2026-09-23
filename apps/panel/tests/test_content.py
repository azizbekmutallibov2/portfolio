import pytest
from django.urls import reverse

from apps.content.models import Project
from apps.content.selectors import site_settings_get
from apps.content.tests.factories import make_project

pytestmark = pytest.mark.django_db


def test_content__anonymous__redirects_to_login():
    from django.test import Client

    response = Client().get(reverse("panel:content"))

    assert response.status_code == 302


def test_content__staff__200(staff_client):
    response = staff_client.get(reverse("panel:content"))

    assert response.status_code == 200


def test_hero_update__valid_data__saves_and_flashes(staff_client):
    response = staff_client.post(
        reverse("panel:hero-update"),
        {
            "hero_line_1": "Yangi 1",
            "hero_line_2": "Yangi 2",
            "about_text": "Yangi tavsif",
            "status_text": "Yangi status",
        },
        follow=True,
    )

    assert response.status_code == 200
    site = site_settings_get()
    assert site.hero_line_1 == "Yangi 1"
    assert b"Hero matni saqlandi." in response.content


def test_hero_update__get__not_allowed(staff_client):
    response = staff_client.get(reverse("panel:hero-update"))

    assert response.status_code == 405


def test_hero_update__invalid_data__shows_errors(staff_client):
    response = staff_client.post(
        reverse("panel:hero-update"),
        {"hero_line_1": "", "hero_line_2": "x", "about_text": "x", "status_text": "x"},
    )

    assert response.status_code == 200


def test_links_update__schemeless_url__gets_https_prefix(staff_client):
    response = staff_client.post(
        reverse("panel:links-update"),
        {
            "github_url": "github.com/azizillo",
            "telegram_url": "",
            "linkedin_url": "",
            "contact_email": "",
            "contact_phone": "",
        },
    )

    assert response.status_code == 302
    site = site_settings_get()
    assert site.github_url == "https://github.com/azizillo"


def test_links_update__invalid_github_host__shows_error(staff_client):
    response = staff_client.post(
        reverse("panel:links-update"),
        {
            "github_url": "gitlab.com/azizillo",
            "telegram_url": "",
            "linkedin_url": "",
            "contact_email": "",
            "contact_phone": "",
        },
    )

    assert response.status_code == 200
    assert b"Havola github.com manziliga olib borishi kerak." in response.content


def test_links_update__invalid_telegram_host__shows_error(staff_client):
    response = staff_client.post(
        reverse("panel:links-update"),
        {
            "github_url": "",
            "telegram_url": "telegram.me/azizillo",
            "linkedin_url": "",
            "contact_email": "",
            "contact_phone": "",
        },
    )

    assert response.status_code == 200
    assert b"Havola t.me manziliga olib borishi kerak." in response.content


def test_links_update__invalid_linkedin_path__shows_error(staff_client):
    response = staff_client.post(
        reverse("panel:links-update"),
        {
            "github_url": "",
            "telegram_url": "",
            "linkedin_url": "linkedin.com/azizillo",
            "contact_email": "",
            "contact_phone": "",
        },
    )

    assert response.status_code == 200
    assert b"Havola linkedin.com manziliga olib borishi kerak." in response.content


def _project_payload(**overrides) -> dict:
    payload = {
        "title": "Yangi loyiha",
        "tag": "production",
        "stack": "Django, PostgreSQL",
        "order": "0",
        "problem": "Muammo matni",
        "solution": "Yechim matni",
        "role": "Rol matni",
        "repo_url": "",
        "demo_url": "",
    }
    payload.update(overrides)
    return payload


def test_project_create__valid_data__creates_project(staff_client):
    response = staff_client.post(reverse("panel:project-create"), _project_payload())

    assert response.status_code == 302
    assert Project.objects.filter(title="Yangi loyiha").exists()


def test_project_create__invalid_data__does_not_create(staff_client):
    response = staff_client.post(reverse("panel:project-create"), _project_payload(title=""))

    assert response.status_code == 200
    assert Project.objects.count() == 0


def test_project_edit__updates_project(staff_client):
    project = make_project(title="Eski nom")

    response = staff_client.post(
        reverse("panel:project-edit", args=[project.pk]),
        _project_payload(title="Yangilangan nom"),
    )

    assert response.status_code == 302
    project.refresh_from_db()
    assert project.title == "Yangilangan nom"


def test_project_edit__get__prefills_form(staff_client):
    project = make_project(title="Ko'rish uchun")

    response = staff_client.get(reverse("panel:project-edit", args=[project.pk]))

    assert response.status_code == 200
    assert b"Ko" in response.content


def test_project_edit__missing__404(staff_client):
    response = staff_client.get(reverse("panel:project-edit", args=[999]))

    assert response.status_code == 404


def test_project_edit__invalid_post_data__rerenders_with_errors(staff_client):
    project = make_project(title="Bor loyiha")

    response = staff_client.post(
        reverse("panel:project-edit", args=[project.pk]), _project_payload(title="")
    )

    assert response.status_code == 200
    project.refresh_from_db()
    assert project.title == "Bor loyiha"


def test_project_delete__removes_project(staff_client):
    project = make_project()

    response = staff_client.post(reverse("panel:project-delete", args=[project.pk]))

    assert response.status_code == 302
    assert not Project.objects.filter(pk=project.pk).exists()


def test_project_delete__missing__404(staff_client):
    response = staff_client.post(reverse("panel:project-delete", args=[999]))

    assert response.status_code == 404
