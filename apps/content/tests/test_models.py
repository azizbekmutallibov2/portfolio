import pytest

from apps.content.selectors import site_settings_get
from apps.content.tests.factories import make_project

pytestmark = pytest.mark.django_db


def test_site_settings__str():
    assert str(site_settings_get()) == "Sayt sozlamalari"


def test_project__str__returns_title():
    project = make_project(title="Mening loyiham")

    assert str(project) == "Mening loyiham"


def test_project__stack_items__splits_and_strips():
    project = make_project(stack="Django, PostgreSQL , Nginx")

    assert project.stack_items == ["Django", "PostgreSQL", "Nginx"]


def test_project__stack_items__empty_stack__returns_empty_list():
    project = make_project(stack="")

    assert project.stack_items == []
