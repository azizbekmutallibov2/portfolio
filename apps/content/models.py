from django.core.validators import MaxLengthValidator
from django.db import models

from apps.content.validators import (
    validate_github_url,
    validate_linkedin_url,
    validate_telegram_url,
)
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_phone


class SiteSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    hero_line_1 = models.CharField(max_length=60, default="Kod yozaman.")
    hero_line_2 = models.CharField(max_length=60, default="Serverga chiqaraman.")
    about_text = models.CharField(
        max_length=300,
        default=(
            "Azizillo. Django va Django REST Framework'da backend yozaman. "
            "TATU, Software Engineering, 1-kurs."
        ),
    )
    status_text = models.CharField(
        max_length=160,
        default="TuitDorm — TATU yotoqxonasini boshqarish tizimi ustida ishlayapman.",
    )
    github_url = models.URLField(blank=True, default="", validators=[validate_github_url])
    telegram_url = models.URLField(blank=True, default="", validators=[validate_telegram_url])
    linkedin_url = models.URLField(blank=True, default="", validators=[validate_linkedin_url])
    contact_email = models.EmailField(blank=True, default="")
    contact_phone = models.CharField(
        max_length=20, blank=True, default="", validators=[validate_phone]
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name="site_settings_singleton"),
        ]

    def __str__(self) -> str:
        return "Sayt sozlamalari"


class ProjectTag(models.TextChoices):
    PRODUCTION = "production", "PRODUCTION"
    TEAM = "team", "GURUH LOYIHASI"
    PERSONAL = "personal", "SHAXSIY LOYIHA"
    LEARNING = "learning", "O'QUV LOYIHASI"


class Project(TimeStampedModel):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    tag = models.CharField(max_length=20, choices=ProjectTag.choices, default=ProjectTag.PRODUCTION)
    problem = models.TextField(validators=[MaxLengthValidator(600)])
    solution = models.TextField(validators=[MaxLengthValidator(600)])
    role = models.CharField(max_length=300)
    stack = models.CharField(max_length=200)
    repo_url = models.URLField(blank=True, default="")
    demo_url = models.URLField(blank=True, default="")
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ["order", "id"]
        indexes = [
            models.Index(fields=["is_published", "order"], name="project_published_order_idx"),
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def stack_items(self) -> list[str]:
        return [item.strip() for item in self.stack.split(",") if item.strip()]
