from django import forms

from apps.contact.validators import validate_contact


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Ism",
        max_length=100,
        min_length=2,
        error_messages={"min_length": "Ism kamida 2 ta harf bo'lsin."},
        widget=forms.TextInput(
            attrs={"autocomplete": "name", "maxlength": "100", "placeholder": "Ismingiz"}
        ),
    )
    contact = forms.CharField(
        label="Telefon yoki email",
        max_length=150,
        validators=[validate_contact],
        widget=forms.TextInput(attrs={"maxlength": "150", "placeholder": "+998 ... yoki email"}),
    )
    message = forms.CharField(
        label="Xabar",
        max_length=2000,
        min_length=10,
        error_messages={"min_length": "Xabar kamida 10 ta belgidan iborat bo'lsin."},
        widget=forms.Textarea(
            attrs={"rows": 4, "maxlength": "2000", "placeholder": "Nima haqida?"}
        ),
    )
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    def mark_invalid_fields(self) -> None:
        for name in self.errors:
            if name in self.fields:
                self.fields[name].widget.attrs["aria-invalid"] = "true"
                self.fields[name].widget.attrs["aria-describedby"] = f"id_{name}-error"
