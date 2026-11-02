"""Rebuild the 2026-11-02 sprite atlas from its preserved registered frames.

Only the jumping and working cells are replaced; every other pixel must match
the specified earlier atlas. This script performs no drawing or pose editing.
"""

import argparse
import hashlib
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
BASE_SHA256 = "1f1047c6999b6f05c80a7846f0b9143c835e704dbaed956d66e40299bbd9f330"
ROWS = (("jumping", 4, 5), ("running", 7, 6))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-atlas", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; keep previous artifacts intact")
    if hashlib.sha256(args.base_atlas.read_bytes()).hexdigest() != BASE_SHA256:
        parser.error("base atlas does not match the recorded 2026-10-28 version")

    with Image.open(args.base_atlas) as source:
        if source.size != (1536, 2288):
            parser.error("base atlas is not the native v2 size")
        original = source.convert("RGBA")
    atlas = original.copy()
    for state, row, count in ROWS:
        folder = HERE / "registered-frames" / state
        files = sorted(folder.glob("*.png"))
        if len(files) != count:
            parser.error(f"{state} needs {count} registered frames")
        for column, file in enumerate(files):
            with Image.open(file) as image:
                if image.size != (192, 208):
                    parser.error(f"invalid frame dimensions: {file}")
                atlas.paste(image.convert("RGBA"), (192 * column, 208 * row))

    for row in (0, 1, 2, 3, 5, 6, 8, 9, 10):
        region = (0, row * 208, 1536, (row + 1) * 208)
        if original.crop(region).tobytes() != atlas.crop(region).tobytes():
            raise RuntimeError(f"unexpected pixel change in row {row}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(args.output, format="WEBP", lossless=True, quality=100, method=6, exact=True)
    with Image.open(args.output) as encoded:
        if encoded.convert("RGBA").tobytes() != atlas.tobytes():
            raise RuntimeError("encoded atlas did not round-trip losslessly")
    print(hashlib.sha256(args.output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
