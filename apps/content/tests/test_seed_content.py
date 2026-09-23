import pytest
from django.core.management import call_command

from apps.content.models import Project, SiteSettings
from apps.content.services import site_settings_update

pytestmark = pytest.mark.django_db


def test_seed_content__run_twice__no_duplicates():
    call_command("seed_content")
    call_command("seed_content")

    assert Project.objects.count() == 2
    assert SiteSettings.objects.count() == 1


def test_seed_content__does_not_overwrite_manual_hero_edit():
    call_command("seed_content")
    site_settings_update(data={"hero_line_1": "Qo'lda kiritilgan"}, fields=["hero_line_1"])

    call_command("seed_content")

    settings_obj = SiteSettings.objects.get(pk=1)
    assert settings_obj.hero_line_1 == "Qo'lda kiritilgan"
