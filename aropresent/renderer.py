import re

COLUMN_MARKER = re.compile(r"^\s*\\col\d+\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


class MarkdownRenderer:
    def __init__(self) -> None:
        try:
            import markdown
        except ModuleNotFoundError as exc:
            raise RuntimeError("Missing dependency 'markdown'. Install requirements.txt first.") from exc
        try:
            import emoji
        except ModuleNotFoundError as exc:
            raise RuntimeError("Missing dependency 'emoji'. Install requirements.txt first.") from exc
        try:
            import pygments
        except ModuleNotFoundError as exc:
            raise RuntimeError("Missing dependency 'Pygments'. Install requirements.txt first.") from exc

        self._emoji = emoji
        self._md = markdown.Markdown(extensions=["extra", "sane_lists", "tables", "codehilite"])

    def render(self, text: str) -> str:
        text = self._emoji.emojize(text, language="alias")
        header, columns = self._split_columns(text)
        if not columns:
            return self._convert(text)
        cells = "".join(f'<div class="column">{self._convert(col)}</div>' for col in columns)
        return f'{self._convert(header)}<div class="columns">{cells}</div>'

    def _convert(self, text: str) -> str:
        return self._md.reset().convert(text)

    @staticmethod
    def _split_columns(text: str) -> tuple[str, list[str]]:
        """Split on \\colN marker lines; text before the first marker is the header."""
        parts: list[list[str]] = [[]]
        in_fence = False
        for line in text.splitlines():
            if FENCE.match(line):
                in_fence = not in_fence
            elif not in_fence and COLUMN_MARKER.match(line):
                parts.append([])
                continue
            parts[-1].append(line)
        header, *columns = ["\n".join(part) for part in parts]
        return header, columns

