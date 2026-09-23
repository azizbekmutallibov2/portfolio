from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from apps.content.models import ProjectTag
from apps.content.validators import (
    validate_github_url,
    validate_linkedin_url,
    validate_telegram_url,
)
from apps.core.validators import validate_phone

LOGIN_ERROR = "Login yoki parol noto'g'ri."


class StaffAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": LOGIN_ERROR,
        "inactive": LOGIN_ERROR,
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login"
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["password"].label = "Parol"
        self.fields["password"].widget.attrs["autocomplete"] = "current-password"

    def confirm_login_allowed(self, user) -> None:
        if not user.is_active or not user.is_staff:
            raise ValidationError(self.error_messages["invalid_login"], code="invalid_login")


class HeroForm(forms.Form):
    hero_line_1 = forms.CharField(label="Sarlavha, 1-qator", max_length=60)
    hero_line_2 = forms.CharField(label="Sarlavha, 2-qator", max_length=60)
    about_text = forms.CharField(
        label="Kim (qisqa ma'lumot)", max_length=300, widget=forms.Textarea(attrs={"rows": 3})
    )
    status_text = forms.CharField(label="Hozir nima ustida", max_length=160)


class LinksForm(forms.Form):
    github_url = forms.CharField(
        label="GitHub havola",
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "github.com/username"}),
    )
    telegram_url = forms.CharField(
        label="Telegram",
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "t.me/username"}),
    )
    linkedin_url = forms.CharField(
        label="LinkedIn",
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "linkedin.com/in/username"}),
    )
    contact_email = forms.EmailField(label="Email", required=False)
    contact_phone = forms.CharField(
        label="Telefon", required=False, max_length=20, validators=[validate_phone]
    )

    @staticmethod
    def _with_scheme(value: str) -> str:
        if value and not value.startswith(("http://", "https://")):
            return f"https://{value}"
        return value

    def clean_github_url(self) -> str:
        value = self._with_scheme(self.cleaned_data.get("github_url", ""))
        if value:
            validate_github_url(value)
        return value

    def clean_telegram_url(self) -> str:
        value = self._with_scheme(self.cleaned_data.get("telegram_url", ""))
        if value:
            validate_telegram_url(value)
        return value

    def clean_linkedin_url(self) -> str:
        value = self._with_scheme(self.cleaned_data.get("linkedin_url", ""))
        if value:
            validate_linkedin_url(value)
        return value


class ProjectForm(forms.Form):
    title = forms.CharField(label="Nom", max_length=120)
    tag = forms.ChoiceField(label="Teg", choices=ProjectTag.choices)
    stack = forms.CharField(
        label="Stack",
        max_length=200,
        help_text="Vergul bilan ajrating: Django, PostgreSQL, Nginx",
    )
    order = forms.IntegerField(label="Tartib", min_value=0, initial=0)
    problem = forms.CharField(
        label="Muammo", max_length=600, widget=forms.Textarea(attrs={"rows": 3})
    )
    solution = forms.CharField(
        label="Yechim", max_length=600, widget=forms.Textarea(attrs={"rows": 3})
    )
    role = forms.CharField(
        label="Mening rolim", max_length=300, widget=forms.Textarea(attrs={"rows": 2})
    )
    is_published = forms.BooleanField(label="Saytda ko'rsatish", required=False)
    repo_url = forms.URLField(label="GitHub havola", required=False, assume_scheme="https")
    demo_url = forms.URLField(label="Demo havola", required=False, assume_scheme="https")
