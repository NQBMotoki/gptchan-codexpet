"""Extract exact encoded action cells for the bundled frame inspector."""

import argparse
import json
from pathlib import Path

from PIL import Image

STATES = (("idle", 6), ("running-right", 8), ("running-left", 8),
          ("waving", 4), ("jumping", 5), ("failed", 8),
          ("waiting", 6), ("running", 6), ("review", 6))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    atlas = Image.open(args.atlas).convert("RGBA")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for row, (state, count) in enumerate(STATES):
        folder = args.output_dir / state
        folder.mkdir(exist_ok=True)
        paths = []
        for col in range(count):
            out = folder / f"{col:02}.png"
            atlas.crop((192 * col, 208 * row, 192 * (col + 1), 208 * (row + 1))).save(out)
            paths.append(str(out))
        rows.append({"state": state, "method": "encoded-atlas", "frames": paths})
    manifest = {"chroma_key": {"hex": "#00FF00", "rgb": [0, 255, 0]}, "rows": rows}
    (args.output_dir / "frames-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {sum(count for _, count in STATES)} original encoded action frames")


if __name__ == "__main__":
    main()
