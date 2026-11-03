"""Document comparable material crops and color samples from encoded frames."""

import argparse
import colorsys
import json
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw


# Crops are approximate hand-selected material regions, not segmentation masks.
SAMPLES = (
    ("hair", "purple", (55, 70, 75, 115), (55, 70, 75, 115)),
    ("left wing", "purple", (30, 75, 55, 105), (25, 35, 50, 65)),
    ("white dress", "white", (78, 96, 110, 127), (78, 90, 110, 121)),
    ("face skin", "skin", (80, 56, 101, 68), (80, 55, 101, 67)),
    ("rose ornament", "purple", (107, 34, 120, 50), (107, 34, 120, 50)),
)


def eligible(pixel, kind):
    r, g, b, a = pixel
    if a < 250:
        return False
    if kind == "purple":
        return b > g + 5 and r > g + 4
    if kind == "white":
        return r > 210 and g > 200 and b > 200
    return r > g + 12 and g > b + 4 and r > 180


def stats(pixels):
    if not pixels:
        raise ValueError("Material sample is empty")
    hsv = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255) for r, g, b, _ in pixels]
    return {
        "pixels": len(pixels),
        "median_rgb": [round(median(p[i] for p in pixels), 2) for i in range(3)],
        "median_hue_degrees": round(median(p[0] for p in hsv) * 360, 2),
        "median_saturation": round(median(p[1] for p in hsv), 4),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, type=Path)
    parser.add_argument("--after", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--json-out", required=True, type=Path)
    args = parser.parse_args()
    before = Image.open(args.before).convert("RGBA")
    after = Image.open(args.after).convert("RGBA")
    idle = before.crop((960, 0, 1152, 208))
    old_jump = before.crop((768, 832, 960, 1040))
    new_jump = after.crop((768, 832, 960, 1040))
    board = Image.new("RGB", (720, 5 * 138 + 24), "#f7f7f7")
    draw = ImageDraw.Draw(board)
    for col, label in enumerate(("idle reference", "wingbeat before", "wingbeat after")):
        draw.text((col * 240 + 95, 4), label, fill="#222222")
    records = []
    for row, (name, kind, idle_box, jump_box) in enumerate(SAMPLES):
        y = 24 + row * 138
        draw.text((3, y + 3), name, fill="#222222")
        images = (idle.crop(idle_box), old_jump.crop(jump_box), new_jump.crop(jump_box))
        for col, crop in enumerate(images):
            # Nearest-neighbor enlargement is for inspection only.
            background = Image.new("RGBA", crop.size, "#f7f7f7")
            background.alpha_composite(crop)
            enlarged = background.resize((crop.width * 3, crop.height * 3), Image.Resampling.NEAREST)
            board.paste(enlarged.convert("RGB"), (col * 240 + 95, y + 3))
        ref, old, new = (list(im.getdata()) for im in images)
        ref_sample = [p for p in ref if eligible(p, kind)]
        selected = [(a, b) for a, b in zip(old, new) if eligible(a, kind)]
        records.append({"material": name, "sample_type": kind, "idle_box": idle_box,
                        "jump_box": jump_box, "idle": stats(ref_sample),
                        "before": stats([a for a, _ in selected]),
                        "after_same_pixels": stats([b for _, b in selected])})
    args.image.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    board.save(args.image)
    args.json_out.write_text(json.dumps({"limitations": "Crops are approximate, distinct poses; material percentages differ. Before/after uses the identical original pixel selection.", "samples": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
