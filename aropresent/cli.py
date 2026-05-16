import argparse
import sys
from pathlib import Path

from .parser import SlideDeck
from .server import WebServerApp


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lightweight .pmd markdown presenter")
    parser.add_argument("file", nargs="?", type=Path, help="Path to .pmd file")
    parser.add_argument("--parse-only", action="store_true", help="Parse and print slide count")
    parser.add_argument(
        "--mode",
        choices=("editor", "present"),
        default="editor",
        help="Run the web editor or the presentation view",
    )
    parser.add_argument("--port", type=int, default=0, help="Port to run the web server on")
    parser.add_argument("--no-open", action="store_true", help="Do not open the browser")
    return parser


def run(args: list[str] | None = None) -> int:
    parsed = build_arg_parser().parse_args(args=args)
    path: Path | None = parsed.file

    if path is not None and not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    deck: SlideDeck | None = None
    if path is not None:
        try:
            deck = SlideDeck.from_file(path)
        except ValueError as exc:
            print(f"Invalid .pmd: {exc}", file=sys.stderr)
            return 2

    if parsed.parse_only:
        if path is None:
            print("Parse-only requires a .pmd file.", file=sys.stderr)
            return 2
        print(f"Slides: {len(deck.slides)}")
        return 0

    if parsed.mode == "present" and deck is None:
        print("Presentation mode requires a .pmd file.", file=sys.stderr)
        return 2

    app = WebServerApp(
        deck=deck,
        title=path.name if path else "AroPresent",
        port=parsed.port,
        mode=parsed.mode,
        open_browser=not parsed.no_open,
    )
    app.run()
    return 0

