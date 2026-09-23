from apps.content.models import Project, ProjectTag


def make_project(**overrides) -> Project:
    defaults = {
        "title": "Test loyiha",
        "slug": "test-loyiha",
        "tag": ProjectTag.PRODUCTION,
        "problem": "Muammo",
        "solution": "Yechim",
        "role": "Rol",
        "stack": "Django",
        "repo_url": "",
        "demo_url": "",
        "order": 0,
        "is_published": True,
    }
    defaults.update(overrides)
    return Project.objects.create(**defaults)
