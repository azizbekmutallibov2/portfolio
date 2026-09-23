from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from apps.contact.validators import validate_contact
from apps.core.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    contact = models.CharField(max_length=150, validators=[validate_contact])
    body = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(2000)])
    is_read = models.BooleanField(default=False)
    ip_hash = models.CharField(max_length=64, blank=True, default="")
    user_agent = models.CharField(max_length=300, blank=True, default="")

    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["ip_hash", "created_at"], name="message_ip_created_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.created_at:%Y-%m-%d})"
