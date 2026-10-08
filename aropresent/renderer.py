import html
import re
from dataclasses import dataclass, field

FENCE = re.compile(r"^\s*(```|~~~)")
COLUMN_MARKER = re.compile(r"^\s*\\col\d+\s*$")
DIV_OPEN = re.compile(r"^\s*\\d\s*$")
DIV_CLOSE = re.compile(r"^\s*\\end\s*$")
STYLE_COMMAND = re.compile(r"^\s*\\(fontsize|color|bg|align|style)\{(.*)\}\s*$")

STYLE_PROPERTIES = {"color": "color", "bg": "background", "align": "text-align"}


@dataclass
class Block:
    """A slide, \\d box, or column: its own styles, its content, and optional columns."""

    kind: str
    styles: list[str] = field(default_factory=list)
    children: list["str | Block"] = field(default_factory=list)
    columns: list["Block"] = field(default_factory=list)

    def add_line(self, line: str) -> None:
        if self.children and isinstance(self.children[-1], str):
            self.children[-1] += "\n" + line
        else:
            self.children.append(line)


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
        return self._render_block(self._parse(text))

    def _convert(self, text: str) -> str:
        return self._md.reset().convert(text)

    @staticmethod
    def _parse(text: str) -> Block:
        """Build the block tree from \\d, \\end, \\colN and style command lines."""
        root = Block("slide")
        stack = [root]
        in_fence = False
        for line in text.splitlines():
            if FENCE.match(line):
                in_fence = not in_fence
                stack[-1].add_line(line)
                continue
            if in_fence:
                stack[-1].add_line(line)
                continue

            if DIV_OPEN.match(line):
                div = Block("div")
                stack[-1].children.append(div)
                stack.append(div)
            elif DIV_CLOSE.match(line):
                if any(block.kind == "div" for block in stack):
                    while stack.pop().kind != "div":
                        pass
            elif COLUMN_MARKER.match(line):
                # Columns split the innermost slide or \d box, not the current column.
                if stack[-1].kind == "column":
                    stack.pop()
                column = Block("column")
                stack[-1].columns.append(column)
                stack.append(column)
            elif match := STYLE_COMMAND.match(line):
                style = MarkdownRenderer._style(match.group(1), match.group(2).strip())
                if style:
                    stack[-1].styles.append(style)
            else:
                stack[-1].add_line(line)
        return root

    @staticmethod
    def _style(command: str, value: str) -> str | None:
        if command == "fontsize":
            try:
                size = float(value)
            except ValueError:
                return None
            return f"font-size: {size:g}px"
        if command == "style":
            return value.rstrip(";")
        return f"{STYLE_PROPERTIES[command]}: {value}"

    def _render_block(self, block: Block) -> str:
        parts = []
        for child in block.children:
            parts.append(self._render_block(child) if isinstance(child, Block) else self._convert(child))
        if block.columns:
            cells = "".join(self._render_block(column) for column in block.columns)
            parts.append(f'<div class="columns">{cells}</div>')
        inner = "".join(parts)

        style = f' style="{html.escape("; ".join(block.styles))}"' if block.styles else ""
        if block.kind == "slide":
            return f'<div class="slide-content"{style}>{inner}</div>' if style else inner
        css_class = "column" if block.kind == "column" else "box"
        return f'<div class="{css_class}"{style}>{inner}</div>'
