import pytest
from django.core.exceptions import ValidationError

from apps.content.models import Project
from apps.content.selectors import site_settings_get
from apps.content.services import (
    normalize_stack,
    project_create,
    project_delete,
    project_update,
    site_settings_update,
)
from apps.content.tests.factories import make_project

pytestmark = pytest.mark.django_db


def test_normalize_stack__dedupes_case_insensitive_and_splits_on_comma_or_dot():
    assert normalize_stack("Django · PostgreSQL, Nginx, django") == "Django, PostgreSQL, Nginx"


def test_normalize_stack__strips_whitespace_and_drops_empty_parts():
    assert normalize_stack("  Django ,, PostgreSQL  ") == "Django, PostgreSQL"


def test_site_settings_update__hero_fields__updates():
    updated, changed = site_settings_update(
        data={"hero_line_1": "Yangi matn"}, fields=["hero_line_1"]
    )

    assert changed is True
    assert updated.hero_line_1 == "Yangi matn"


def test_site_settings_update__mixed_groups__raises_value_error():
    with pytest.raises(ValueError):
        site_settings_update(
            data={"hero_line_1": "x", "github_url": "https://github.com/x"},
            fields=["hero_line_1", "github_url"],
        )


def test_site_settings_update__unknown_field__raises_value_error():
    with pytest.raises(ValueError):
        site_settings_update(data={"not_a_field": "x"}, fields=["not_a_field"])


def test_site_settings_update__invalid_url__raises_validation_error():
    with pytest.raises(ValidationError):
        site_settings_update(data={"github_url": "https://gitlab.com/x"}, fields=["github_url"])


def test_site_settings_update__no_changes__instance_unchanged():
    site_settings_get()

    updated, changed = site_settings_update(
        data={"hero_line_1": "Kod yozaman."}, fields=["hero_line_1"]
    )

    assert changed is False
    assert updated.hero_line_1 == "Kod yozaman."


def _project_kwargs(**overrides) -> dict:
    defaults = {
        "title": "Loyiha",
        "problem": "Muammo",
        "solution": "Yechim",
        "role": "Rol",
        "stack": "Django",
    }
    defaults.update(overrides)
    return defaults


def test_project_create__generates_slug_from_title():
    project = project_create(**_project_kwargs(title="O'zbekiston Kitobxonlari Jamiyati"))

    assert project.slug == "ozbekiston-kitobxonlari-jamiyati"


def test_project_create__duplicate_title__appends_counter():
    first = project_create(**_project_kwargs(title="Loyiha"))
    second = project_create(**_project_kwargs(title="Loyiha"))

    assert first.slug == "loyiha"
    assert second.slug == "loyiha-2"


def test_project_create__cyrillic_title__falls_back_to_loyiha():
    project = project_create(**_project_kwargs(title="Проект"))

    assert project.slug == "loyiha"


def test_project_create__normalizes_stack():
    project = project_create(**_project_kwargs(stack="Django, django, PostgreSQL"))

    assert project.stack == "Django, PostgreSQL"


def test_project_create__blank_title__raises_validation_error():
    with pytest.raises(ValidationError):
        project_create(**_project_kwargs(title=""))


def test_project_update__does_not_change_slug():
    project = make_project(slug="original-slug")

    updated, _ = project_update(project=project, data={"title": "Yangi nom", "slug": "hacked"})

    assert updated.slug == "original-slug"
    assert updated.title == "Yangi nom"


def test_project_update__normalizes_stack():
    project = make_project(stack="Django")

    updated, _ = project_update(project=project, data={"stack": "Django, django, Nginx"})

    assert updated.stack == "Django, Nginx"


def test_project_update__no_changes__save_not_needed():
    project = make_project(title="Loyiha")

    updated, changed = project_update(project=project, data={"title": "Loyiha"})

    assert changed is False


def test_project_delete__removes_project():
    project = make_project(slug="to-delete")

    project_delete(project=project)

    assert not Project.objects.filter(slug="to-delete").exists()
