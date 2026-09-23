import re
from pathlib import Path

from django.conf import settings
from django.urls import Resolver404, resolve

from apps.public.static_content import INFRA_ENDPOINTS

INLINE_STYLE_RE = re.compile(r'style\s*=\s*"')
INLINE_SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>")


def _template_files():
    templates_dir = Path(settings.BASE_DIR) / "templates"
    return list(templates_dir.rglob("*.html"))


def test_templates_have_no_inline_styles_or_scripts():
    offenders = []
    for path in _template_files():
        text = path.read_text(encoding="utf-8")
        if INLINE_STYLE_RE.search(text) or INLINE_SCRIPT_RE.search(text):
            offenders.append(str(path))

    assert offenders == []


def test_infra_endpoints_are_real():
    for endpoint in INFRA_ENDPOINTS:
        path = endpoint.path.replace("{slug}", "sample")
        try:
            match = resolve(path)
        except Resolver404:
            raise AssertionError(f"{endpoint.path} does not resolve") from None
        assert f"{match.namespace}:{match.url_name}" == endpoint.url_name
