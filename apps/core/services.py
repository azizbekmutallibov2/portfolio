from django.db.models import Model


def model_update(*, instance: Model, fields: list[str], data: dict) -> tuple[Model, bool]:
    changed = []
    for field in fields:
        if field in data and getattr(instance, field) != data[field]:
            setattr(instance, field, data[field])
            changed.append(field)
    if changed:
        instance.full_clean()
        if any(f.name == "updated_at" for f in instance._meta.fields):
            changed.append("updated_at")
        instance.save(update_fields=changed)
    return instance, bool(changed)
