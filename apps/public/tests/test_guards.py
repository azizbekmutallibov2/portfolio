import re
from pathlib import Path

from django.conf import settings

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


# test_infra_endpoints_are_real (architecture.md §12) is added in Phase 4:
# static_content.INFRA_ENDPOINTS references api:project-list, api:project-detail
# and api:contact-create, which do not exist until the API phase. Only api:health
# exists so far (Phase 0). See docs/process.md Phase 2 entry.
