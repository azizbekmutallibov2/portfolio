import pytest

from apps.contact.models import ContactMessage

VALID_PAYLOAD = {
    "name": "Ali",
    "contact": "ali@example.com",
    "message": "Bu test xabari, kamida o'nta belgi.",
}


@pytest.mark.django_db
def test_contact_create__valid__returns_201_and_saves(api_client):
    response = api_client.post("/api/v1/contact/", VALID_PAYLOAD, format="json")

    assert response.status_code == 201
    assert response.json() == {"detail": "Xabar qabul qilindi."}
    assert ContactMessage.objects.count() == 1


@pytest.mark.django_db
def test_contact_create__invalid_contact__returns_400_and_does_not_save(api_client):
    payload = {**VALID_PAYLOAD, "contact": "not-a-contact"}

    response = api_client.post("/api/v1/contact/", payload, format="json")

    assert response.status_code == 400
    assert "contact" in response.json()
    assert ContactMessage.objects.count() == 0


@pytest.mark.django_db
def test_contact_create__missing_fields__returns_400(api_client):
    response = api_client.post("/api/v1/contact/", {}, format="json")

    assert response.status_code == 400
    body = response.json()
    assert "name" in body
    assert "contact" in body
    assert "message" in body


@pytest.mark.django_db
def test_contact_create__over_limit__returns_429(api_client, settings):
    settings.CONTACT_RATE_LIMIT_PER_HOUR = 1
    api_client.post("/api/v1/contact/", VALID_PAYLOAD, format="json")

    response = api_client.post(
        "/api/v1/contact/",
        {**VALID_PAYLOAD, "contact": "other@example.com"},
        format="json",
    )

    assert response.status_code == 429
    assert "detail" in response.json()
    assert ContactMessage.objects.count() == 1


@pytest.mark.django_db
def test_contact_create__wrong_method__returns_405(api_client):
    response = api_client.get("/api/v1/contact/")

    assert response.status_code == 405
