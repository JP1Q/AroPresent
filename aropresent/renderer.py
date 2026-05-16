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
        return self._md.reset().convert(text)
