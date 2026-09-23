from apps.contact.models import ContactMessage


def make_message(**overrides) -> ContactMessage:
    defaults = {
        "name": "Test Foydalanuvchi",
        "contact": "test@example.com",
        "body": "Bu test xabari, kamida o'nta belgi.",
        "is_read": False,
        "ip_hash": "",
        "user_agent": "",
    }
    defaults.update(overrides)
    return ContactMessage.objects.create(**defaults)
