import html
from pathlib import Path

HTML_DIR = Path(__file__).resolve().parent / "html"
SLIDE_TEMPLATES_DIR = Path(__file__).resolve().parent / "slide_templates"


def _load(name: str, title: str) -> str:
    template = (HTML_DIR / name).read_text(encoding="utf-8")
    return template.replace("__TITLE__", html.escape(title))


def build_editor_html(title: str) -> str:
    return _load("editor.html", title)


def build_present_html(title: str) -> str:
    return _load("present.html", title)


def load_slide_templates() -> list[dict]:
    """Read slide_templates/*.md; "4-two-columns.md" becomes id "two-columns", label "Two Columns Slide"."""
    entries = []
    for file in SLIDE_TEMPLATES_DIR.glob("*.md"):
        order, _, name = file.stem.partition("-")
        if order.isdigit() and name:
            entries.append((int(order), name, file))
        else:
            entries.append((float("inf"), file.stem, file))

    templates = []
    for _, name, file in sorted(entries):
        templates.append({
            "id": name,
            "label": name.replace("-", " ").title() + " Slide",
            "content": file.read_text(encoding="utf-8"),
        })
    return templates
