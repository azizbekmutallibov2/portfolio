from types import SimpleNamespace
from unittest.mock import Mock

from apps.core.services import model_update


def _fake_instance(*, has_updated_at: bool, **initial):
    fields = [SimpleNamespace(name=name) for name in initial]
    if has_updated_at:
        fields.append(SimpleNamespace(name="updated_at"))
    instance = Mock(spec=[*initial.keys(), "full_clean", "save", "_meta"])
    for key, value in initial.items():
        setattr(instance, key, value)
    instance._meta = SimpleNamespace(fields=fields)
    return instance


def test_model_update__no_changes__does_not_save():
    instance = _fake_instance(has_updated_at=True, title="Hello")

    updated, changed = model_update(instance=instance, fields=["title"], data={"title": "Hello"})

    assert updated is instance
    assert changed is False
    instance.full_clean.assert_not_called()
    instance.save.assert_not_called()


def test_model_update__field_changed__saves_and_calls_full_clean():
    instance = _fake_instance(has_updated_at=True, title="Old")

    updated, changed = model_update(instance=instance, fields=["title"], data={"title": "New"})

    assert updated.title == "New"
    assert changed is True
    instance.full_clean.assert_called_once()
    instance.save.assert_called_once_with(update_fields=["title", "updated_at"])


def test_model_update__no_updated_at_field__save_fields_do_not_include_it():
    instance = _fake_instance(has_updated_at=False, title="Old")

    model_update(instance=instance, fields=["title"], data={"title": "New"})

    instance.save.assert_called_once_with(update_fields=["title"])


def test_model_update__field_not_in_data__ignored():
    instance = _fake_instance(has_updated_at=True, title="Old", role="Dev")

    updated, changed = model_update(
        instance=instance, fields=["title", "role"], data={"title": "Old"}
    )

    assert changed is False
    assert updated.role == "Dev"
