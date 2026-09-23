from unittest.mock import patch

import pytest


@pytest.mark.django_db
def test_health__database_ok__returns_200(api_client):
    response = api_client.get("/api/v1/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


@pytest.mark.django_db
def test_health__database_error__returns_503(api_client):
    with patch("apps.api.views.connection.cursor", side_effect=Exception("boom")):
        response = api_client.get("/api/v1/health/")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "error"}
