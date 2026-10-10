"""Inline Lucide icons (ISC license, see scripts/lucide/LICENSE)."""
import re
from functools import lru_cache
from pathlib import Path

LUCIDE = Path(__file__).resolve().parent / "lucide"


@lru_cache(maxsize=None)
def _inner(name):
    svg = (LUCIDE / f"{name}.svg").read_text(encoding="utf-8")
    body = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    return re.sub(r"\s*\n\s*", "", body)


def icon(name, cls="ico"):
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_inner(name)}</svg>'
    )


def fill_icons(html):
    """Replaces {{ICON:name}} and {{ICON:name:class}} placeholders."""
    return re.sub(r"\{\{ICON:([a-z0-9-]+)(?::([a-z0-9 -]+))?\}\}", lambda m: icon(m.group(1), m.group(2) or "ico"), html)
