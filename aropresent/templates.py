import html
import json
from pathlib import Path

VIEWS_DIR = Path(__file__).resolve().parent / "views"
SLIDE_TEMPLATES_DIR = Path(__file__).resolve().parent / "slide_templates"


def _load(view: str, title: str) -> str:
    template = (VIEWS_DIR / view / f"{view}.html").read_text(encoding="utf-8")
    return template.replace("__TITLE__", html.escape(title))


def build_editor_html(title: str) -> str:
    return _load("editor", title)


def build_present_html(title: str) -> str:
    return _load("present", title)


def load_slide_templates() -> list[dict]:
    """Templates in the order and with the labels given by slide_templates/templates.json."""
    order = json.loads((SLIDE_TEMPLATES_DIR / "templates.json").read_text(encoding="utf-8"))
    templates = []
    for entry in order:
        print(entry)
        file = SLIDE_TEMPLATES_DIR / entry["file"]
        templates.append({
            "id": file.stem,
            "label": entry.get("label", file.stem),
            "content": file.read_text(encoding="utf-8"),
        })
    return templates
