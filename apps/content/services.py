import re

from django.utils.text import slugify

from apps.content.models import Project, ProjectTag, SiteSettings
from apps.content.selectors import site_settings_get
from apps.core.services import model_update

HERO_FIELDS = ["hero_line_1", "hero_line_2", "about_text", "status_text"]
LINK_FIELDS = ["github_url", "telegram_url", "linkedin_url", "contact_email", "contact_phone"]
PROJECT_UPDATABLE_FIELDS = [
    "title",
    "tag",
    "problem",
    "solution",
    "role",
    "stack",
    "repo_url",
    "demo_url",
    "order",
    "is_published",
]

_STACK_SPLIT_RE = re.compile(r"[,·]")


def normalize_stack(value: str) -> str:
    seen: set[str] = set()
    result: list[str] = []
    for part in _STACK_SPLIT_RE.split(value):
        cleaned = part.strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(cleaned)
    return ", ".join(result)


def site_settings_update(*, data: dict, fields: list[str]) -> tuple[SiteSettings, bool]:
    fields_set = set(fields)
    if not (fields_set <= set(HERO_FIELDS) or fields_set <= set(LINK_FIELDS)):
        raise ValueError("Ruxsatsiz maydon.")
    instance = site_settings_get()
    return model_update(instance=instance, fields=fields, data=data)


def project_create(
    *,
    title: str,
    problem: str,
    solution: str,
    role: str,
    stack: str,
    tag: str = ProjectTag.PRODUCTION,
    repo_url: str = "",
    demo_url: str = "",
    order: int = 0,
    is_published: bool = True,
) -> Project:
    base_slug = slugify(title)[:120] or "loyiha"
    slug = base_slug
    counter = 2
    while Project.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    project = Project(
        title=title.strip(),
        slug=slug,
        tag=tag,
        problem=problem,
        solution=solution,
        role=role,
        stack=normalize_stack(stack),
        repo_url=repo_url,
        demo_url=demo_url,
        order=order,
        is_published=is_published,
    )
    project.full_clean()
    project.save()
    return project


def project_update(*, project: Project, data: dict) -> tuple[Project, bool]:
    fields = [field for field in PROJECT_UPDATABLE_FIELDS if field in data]
    update_data = dict(data)
    if "stack" in update_data:
        update_data["stack"] = normalize_stack(update_data["stack"])
    return model_update(instance=project, fields=fields, data=update_data)


def project_delete(*, project: Project) -> None:
    project.delete()
