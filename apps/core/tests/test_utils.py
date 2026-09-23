from django.test import RequestFactory

from apps.core.utils import get_client_ip, hash_ip


def test_get_client_ip__x_real_ip_present__returns_it():
    request = RequestFactory().get("/", HTTP_X_REAL_IP="203.0.113.5", REMOTE_ADDR="10.0.0.1")

    assert get_client_ip(request) == "203.0.113.5"


def test_get_client_ip__x_real_ip_missing__falls_back_to_remote_addr():
    request = RequestFactory().get("/", REMOTE_ADDR="10.0.0.1")

    assert get_client_ip(request) == "10.0.0.1"


def test_get_client_ip__nothing_present__returns_empty_string():
    request = RequestFactory().get("/")
    request.META.pop("REMOTE_ADDR", None)

    assert get_client_ip(request) == ""


def test_hash_ip__deterministic():
    assert hash_ip("203.0.113.5") == hash_ip("203.0.113.5")


def test_hash_ip__differs_from_raw_ip():
    assert hash_ip("203.0.113.5") != "203.0.113.5"


def test_hash_ip__different_ips_differ():
    assert hash_ip("203.0.113.5") != hash_ip("203.0.113.6")
