from apps.core.exceptions import ApplicationError


def test_application_error__stores_message_and_extra():
    error = ApplicationError("Xatolik yuz berdi.", extra={"field": "name"})

    assert str(error) == "Xatolik yuz berdi."
    assert error.message == "Xatolik yuz berdi."
    assert error.extra == {"field": "name"}


def test_application_error__no_extra__defaults_to_empty_dict():
    error = ApplicationError("Xatolik.")

    assert error.extra == {}
