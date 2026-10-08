# /// script
# requires-python = ">=3.11"
# dependencies = ["athanor @ git+https://github.com/script-wizards/athanor"]
# ///
"""Render the tarot cards that `draw` shows.

Uses Athanor's deck and its Commons fetcher:

    uv run tools/tarot.py [scan dir]

Each card is dithered the way Athanor's lockscreen card is, then saved as a
two-color PNG whose paper is opaque and whose lines are transparent. The page
uses it as a CSS mask and picks the colors itself.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from athanor import tarot

WIDTH = 80
HEIGHT = 140
SCALE = 2
OUT = Path(__file__).resolve().parent.parent / "tarot"


def render(src: Path, out: Path) -> None:
    subprocess.run(
        [
            "magick", str(src),
            "-colorspace", "HSL", "-channel", "B", "-separate", "+channel",
            "-resize", f"{WIDTH}x", "-gamma", "1.4",
            "-dither", "FloydSteinberg", "-monochrome",
            "-background", "white", "-gravity", "center", "-extent", f"{WIDTH}x{HEIGHT}",
            "-filter", "point", "-resize", f"{SCALE * 100}%",
            "-transparent", "black", "-strip", f"PNG8:{out}",
        ],
        check=True,
    )  # fmt: skip


def main() -> None:
    scans = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
    tarot.fetch_art(scans)
    OUT.mkdir(exist_ok=True)
    for card in tarot.DECK:
        render(tarot.art_path(card, scans), OUT / f"{card.index:02d}.png")
    print(f"{len(tarot.DECK)} cards in {OUT}")


if __name__ == "__main__":
    main()
