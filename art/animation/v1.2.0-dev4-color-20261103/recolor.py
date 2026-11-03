"""Rebuild dev.3 with a reversible, color-only grade on the five wingbeat frames.

The user explicitly requested numerical adjustment without new image generation.
This works on the existing straight-alpha pixels; it neither invents shapes nor
changes the alpha, registration, timing, other action rows, or gaze directions.
"""

import argparse
import colorsys
import hashlib
import json
from pathlib import Path
from statistics import median

from PIL import Image


BASE_SHA256 = "6756813298bf70fd7cf09e97b7f62e1e8bb88a34ced95c72b7cd0161e03ffea4"
CELL_W, CELL_H = 192, 208
JUMP_ROW, JUMP_COUNT = 4, 5
HUE_STOPS = ((0, 0), (265, 8), (280, 16), (300, 23), (320, 30), (360, 30))


def smoothstep(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def hue_shift(hue):
    for (lo, start), (hi, end) in zip(HUE_STOPS, HUE_STOPS[1:]):
        if hue <= hi:
            return start + (end - start) * (hue - lo) / (hi - lo)
    return HUE_STOPS[-1][1]


def grade_pixel(pixel):
    r, g, b, alpha = pixel
    if alpha == 0:
        return pixel
    hue, sat, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    degrees = hue * 360

    # Smooth weights avoid hard transitions at the edges of the lavender mask.
    # Cool purple hair, wing membranes, fabric shadows and purple outlines.
    purple = (smoothstep((degrees - 250) / 28)
              * smoothstep((360 - degrees) / 15)
              * smoothstep((sat - 0.035) / 0.085))
    new_hue = (degrees - hue_shift(degrees) * purple) / 360
    new_sat = sat * (1 - 0.17 * purple)

    # Gently bring peach skin closer to the idle reference without touching
    # near-white highlights or inventing a new material/outline.
    skin = (smoothstep(degrees / 5)
            * smoothstep((47 - degrees) / 17)
            * smoothstep((sat - 0.07) / 0.10))
    new_hue = (new_hue + skin * 1.5 / 360) % 1
    new_sat *= 1 - 0.12 * skin
    if purple == 0 and skin == 0:
        return pixel
    out = colorsys.hsv_to_rgb(new_hue, new_sat, value)
    return tuple(round(channel * 255) for channel in out) + (alpha,)


def purple_sample(original, result):
    """Compare the same original selected pixels, so the mask cannot drift."""
    before, after = [], []
    for old, new in zip(original.getdata(), result.getdata()):
        r, g, b, alpha = old
        if alpha >= 250 and b > g + 15 and r > g + 8 and 50 <= g <= 205 and b < 245:
            before.append(old)
            after.append(new)

    def stats(pixels):
        hues, sats, red_minus_blue = [], [], []
        for r, g, b, _ in pixels:
            h, s, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            hues.append(h * 360)
            sats.append(s)
            red_minus_blue.append(r - b)
        return {"hue_degrees": round(median(hues), 3),
                "saturation": round(median(sats), 4),
                "red_minus_blue": round(median(red_minus_blue), 3)}

    return {"selected_opaque_pixels": len(before), "before": stats(before), "after": stats(after)}


def rgba_digest(image):
    return hashlib.sha256(image.tobytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-atlas", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--frames-dir", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if hashlib.sha256(args.base_atlas.read_bytes()).hexdigest() != BASE_SHA256:
        parser.error("base atlas is not the recorded 1.2.0-dev.3 artifact")
    if args.output.exists() or args.report.exists():
        parser.error("output/report already exists; retain previous candidates")
    base = Image.open(args.base_atlas).convert("RGBA")
    if base.size != (1536, 2288):
        parser.error("expected a 1536x2288 v2 atlas")
    result = base.copy()
    args.frames_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for col in range(JUMP_COUNT):
        box = (col * CELL_W, JUMP_ROW * CELL_H, (col + 1) * CELL_W, (JUMP_ROW + 1) * CELL_H)
        original = base.crop(box)
        graded = Image.new("RGBA", original.size)
        graded.putdata([grade_pixel(p) for p in original.getdata()])
        if graded.getchannel("A").tobytes() != original.getchannel("A").tobytes():
            raise RuntimeError("alpha changed")
        graded.save(args.frames_dir / f"{col:02}.png")
        result.paste(graded, (box[0], box[1]))
        info = purple_sample(original, graded)
        info["frame"] = col + 1
        info["changed_rgb_pixels"] = sum(a[:3] != b[:3] for a, b in zip(original.getdata(), graded.getdata()))
        rows.append(info)

    for row in range(11):
        if row == JUMP_ROW:
            continue
        box = (0, row * CELL_H, 1536, (row + 1) * CELL_H)
        if base.crop(box).tobytes() != result.crop(box).tobytes():
            raise RuntimeError(f"untouched atlas row {row} changed")
    if base.getchannel("A").tobytes() != result.getchannel("A").tobytes():
        raise RuntimeError("atlas alpha changed")
    # The three unused cells of the jumping row must be bit-identical too.
    unused = (JUMP_COUNT * CELL_W, JUMP_ROW * CELL_H, 1536, (JUMP_ROW + 1) * CELL_H)
    if base.crop(unused).tobytes() != result.crop(unused).tobytes():
        raise RuntimeError("unused jump cells changed")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output, format="WEBP", lossless=True, quality=100, method=6, exact=True)
    if Image.open(args.output).convert("RGBA").tobytes() != result.tobytes():
        raise RuntimeError("WebP encoding changed RGBA pixels")
    report = {
        "base_file_sha256": BASE_SHA256,
        "output_file_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
        "base_rgba_sha256": rgba_digest(base),
        "output_rgba_sha256": rgba_digest(result),
        "method": "same smooth per-color HSV transform on each original frame",
        "alpha_identical": True,
        "other_ten_rows_rgba_identical": True,
        "jump_unused_cells_rgba_identical": True,
        "selected_pixels": "original alpha>=250, B>G+15, R>G+8, 50<=G<=205, B<245",
        "frames": rows,
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
