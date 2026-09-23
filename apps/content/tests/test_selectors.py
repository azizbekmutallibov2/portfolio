import pytest

from apps.content.models import SiteSettings
from apps.content.selectors import project_counts, project_get, project_list, site_settings_get
from apps.content.tests.factories import make_project

pytestmark = pytest.mark.django_db


def test_site_settings_get__creates_when_missing():
    settings_obj = site_settings_get()

    assert settings_obj.pk == 1


def test_site_settings_get__row_deleted__recreates_it():
    site_settings_get()
    SiteSettings.objects.filter(pk=1).delete()

    settings_obj = site_settings_get()

    assert settings_obj.pk == 1
    assert SiteSettings.objects.count() == 1


def test_project_list__published_only_default__excludes_unpublished():
    published = make_project(slug="published", is_published=True, order=1)
    make_project(slug="unpublished", is_published=False, order=0)

    result = list(project_list())

    assert result == [published]


def test_project_list__ordered_by_order_then_id():
    second = make_project(slug="second", order=2)
    first = make_project(slug="first", order=1)

    assert list(project_list(published_only=False)) == [first, second]


def test_project_list__published_only_false__returns_all():
    make_project(slug="a", is_published=True)
    make_project(slug="b", is_published=False)

    assert project_list(published_only=False).count() == 2


def test_project_get__missing__returns_none():
    assert project_get(slug="missing") is None


def test_project_get__by_pk__returns_project():
    project = make_project(slug="by-pk")

    assert project_get(pk=project.pk) == project


def test_project_get__neither_pk_nor_slug__returns_none():
    make_project(slug="irrelevant")

    assert project_get() is None


def test_project_get__unpublished_with_published_only__returns_none():
    make_project(slug="hidden", is_published=False)

    assert project_get(slug="hidden") is None
    assert project_get(slug="hidden", published_only=False) is not None


def test_project_counts__single_query(django_assert_num_queries):
    make_project(slug="a", is_published=True)
    make_project(slug="b", is_published=False)

    with django_assert_num_queries(1):
        counts = project_counts()

    assert counts == {"total": 2, "published": 1}
