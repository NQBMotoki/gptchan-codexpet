"""Rebuild the grounded-wingbeat atlas from its five preserved encoded cells."""

import argparse
import hashlib
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
BASE_SHA256 = "b3a521ed88820aa4d5aa2d7bf70f003fbcec6c7ea36f398f4a5f0abdfd3307aa"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-atlas", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; retain previous artifacts")
    if hashlib.sha256(args.base_atlas.read_bytes()).hexdigest() != BASE_SHA256:
        parser.error("base atlas does not match the approved eight-action version")
    with Image.open(args.base_atlas) as source:
        if source.size != (1536, 2288):
            parser.error("expected a native v2 atlas")
        original = source.convert("RGBA")
    atlas = original.copy()
    for column in range(5):
        with Image.open(HERE / "encoded-frames-07" / "jumping" / f"{column:02}.png") as image:
            if image.size != (192, 208):
                parser.error(f"unexpected dimensions for frame {column}")
            atlas.paste(image.convert("RGBA"), (192 * column, 4 * 208))
    for row in (0, 1, 2, 3, 5, 6, 7, 8, 9, 10):
        bounds = (0, row * 208, 1536, (row + 1) * 208)
        if original.crop(bounds).tobytes() != atlas.crop(bounds).tobytes():
            raise RuntimeError(f"unexpected change in row {row}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(args.output, format="WEBP", lossless=True, quality=100, method=6, exact=True)
    with Image.open(args.output) as saved:
        if saved.convert("RGBA").tobytes() != atlas.tobytes():
            raise RuntimeError("WebP did not preserve the decoded pixels")
    print(hashlib.sha256(args.output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
