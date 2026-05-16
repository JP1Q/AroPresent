from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aropresent.parser import SlideDeck


def main() -> int:
    deck = SlideDeck.from_file(Path("example.pmd"))
    print(f"Slides: {len(deck.slides)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
