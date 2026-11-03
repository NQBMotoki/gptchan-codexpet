"""Combine dev.2 actions with the user's approved Candidate 08 gaze rows."""

import argparse
import hashlib
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
BASE_SHA256 = "41c8c08d51b1a59197263dfd5b8b1e6bbb221bd7c55b2d51d2be1f3cb3a6cf93"
GAZE_RGBA_SHA256 = "66988e74410af6141a059854e5824c6ada6dfd29042cd089d3eb3792b8979cb4"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-atlas", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; keep previous artifacts intact")
    if hashlib.sha256(args.base_atlas.read_bytes()).hexdigest() != BASE_SHA256:
        parser.error("base atlas must be the recorded 1.2.0-dev.2 artwork")
    with Image.open(args.base_atlas) as image:
        base = image.convert("RGBA")
    with Image.open(HERE / "sources/approved-gaze-rows.png") as image:
        gaze = image.convert("RGBA")
    if base.size != (1536, 2288) or gaze.size != (1536, 416):
        parser.error("unexpected v2 atlas or gaze-row dimensions")
    if hashlib.sha256(gaze.tobytes()).hexdigest() != GAZE_RGBA_SHA256:
        parser.error("gaze pixels differ from the approved Candidate 08")

    result = base.copy()
    result.paste(gaze, (0, 1872))
    if result.crop((0, 0, 1536, 1872)).tobytes() != base.crop((0, 0, 1536, 1872)).tobytes():
        raise RuntimeError("an action row changed during assembly")
    if result.crop((0, 1872, 1536, 2288)).tobytes() != gaze.tobytes():
        raise RuntimeError("the approved gaze pixels changed during assembly")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output, format="WEBP", lossless=True, quality=100, method=6, exact=True)
    with Image.open(args.output) as image:
        if image.convert("RGBA").tobytes() != result.tobytes():
            raise RuntimeError("WebP encoding did not preserve all RGBA pixels")
    print(hashlib.sha256(args.output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
