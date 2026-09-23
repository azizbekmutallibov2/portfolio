import pytest

from apps.core.templatetags.url_tags import display_url


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("https://www.github.com/x/", "github.com/x"),
        ("https://github.com/x", "github.com/x"),
        ("https://t.me/username", "t.me/username"),
        ("https://www.linkedin.com/in/username", "linkedin.com/in/username"),
        ("https://github.com", "github.com"),
        ("", ""),
        (None, ""),
    ],
)
def test_display_url__variants(value, expected):
    assert display_url(value) == expected
