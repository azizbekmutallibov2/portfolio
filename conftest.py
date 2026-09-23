import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient


@pytest.fixture
def staff_user(db):
    return get_user_model().objects.create_user(
        username="staff",
        password="password123",
        is_staff=True,  # noqa: S106
    )


@pytest.fixture
def regular_user(db):
    return get_user_model().objects.create_user(
        username="regular",
        password="password123",  # noqa: S106
    )


@pytest.fixture
def staff_client(staff_user):
    client = Client()
    client.force_login(staff_user)
    return client


@pytest.fixture
def api_client():
    return APIClient()
