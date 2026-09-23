from django.db.models import Count, Q, QuerySet

from apps.content.models import Project, SiteSettings


def site_settings_get() -> SiteSettings:
    return SiteSettings.objects.get_or_create(pk=1)[0]


def project_list(*, published_only: bool = True) -> QuerySet[Project]:
    qs = Project.objects.all()
    if published_only:
        qs = qs.filter(is_published=True)
    return qs


def project_get(
    *, pk: int | None = None, slug: str | None = None, published_only: bool = True
) -> Project | None:
    qs = Project.objects.all()
    if published_only:
        qs = qs.filter(is_published=True)
    if pk is not None:
        return qs.filter(pk=pk).first()
    if slug is not None:
        return qs.filter(slug=slug).first()
    return None


def project_counts() -> dict:
    return Project.objects.aggregate(
        total=Count("id"),
        published=Count("id", filter=Q(is_published=True)),
    )
