import pytest

from apps.content.tests.factories import make_project

PROJECT_FIELDS = {
    "slug",
    "title",
    "tag",
    "tag_label",
    "problem",
    "solution",
    "role",
    "stack",
    "repo_url",
    "demo_url",
}


@pytest.mark.django_db
def test_project_list__only_published_and_ordered__returns_them(api_client):
    make_project(slug="second", order=2, is_published=True)
    make_project(slug="first", order=0, is_published=True)
    make_project(slug="hidden", order=1, is_published=False)

    response = api_client.get("/api/v1/projects/")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert [item["slug"] for item in data["results"]] == ["first", "second"]


@pytest.mark.django_db
def test_project_list__response_shape__matches_spec_and_stack_is_list(api_client):
    make_project(slug="shape", stack="Django, DRF, PostgreSQL")

    response = api_client.get("/api/v1/projects/")

    project = response.json()["results"][0]
    assert set(project.keys()) == PROJECT_FIELDS
    assert project["stack"] == ["Django", "DRF", "PostgreSQL"]
    assert project["tag_label"]


@pytest.mark.django_db
def test_project_list__wrong_method__returns_405(api_client):
    response = api_client.post("/api/v1/projects/")

    assert response.status_code == 405


@pytest.mark.django_db
def test_project_detail__published__returns_200(api_client):
    make_project(slug="visible", is_published=True)

    response = api_client.get("/api/v1/projects/visible/")

    assert response.status_code == 200
    assert response.json()["slug"] == "visible"


@pytest.mark.django_db
def test_project_detail__unpublished__returns_404(api_client):
    make_project(slug="hidden", is_published=False)

    response = api_client.get("/api/v1/projects/hidden/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_project_detail__missing__returns_404(api_client):
    response = api_client.get("/api/v1/projects/does-not-exist/")

    assert response.status_code == 404
