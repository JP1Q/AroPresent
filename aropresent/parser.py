from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Slide:
    content: str
    animation: str = "none"


@dataclass(frozen=True)
class SlideDeck:
    slides: list[Slide]

    @staticmethod
    def from_file(path: Path) -> "SlideDeck":
        text = path.read_text(encoding="utf-8")
        slides = SlideParser.parse(text)
        if not slides:
            raise ValueError("No slides found. Ensure slides are wrapped in { } on their own lines.")
        return SlideDeck(slides=slides)


class SlideParser:
    @staticmethod
    def parse(text: str) -> list[Slide]:
        lines = text.splitlines()
        slides: list[Slide] = []
        buffer: list[str] = []
        in_slide = False
        animation = "none"

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("{"):
                if in_slide:
                    raise ValueError("Nested '{' found. Slides cannot be nested.")
                in_slide = True
                animation = stripped[1:].strip() or "none"
                buffer = []
                continue
            if stripped == "}":
                if not in_slide:
                    raise ValueError("Unmatched '}' found.")
                in_slide = False
                slides.append(Slide(content="\n".join(buffer).strip(), animation=animation))
                buffer = []
                continue
            if in_slide:
                buffer.append(line)

        if in_slide:
            raise ValueError("Missing closing '}' for the final slide.")

        return slides
