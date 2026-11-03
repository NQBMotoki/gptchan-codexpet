"""Render comparison artifacts from the original and final encoded atlases."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 192, 208
LIGHT, DARK = "#f7f7f7", "#26242c"


def cell(atlas, row, col):
    return atlas.crop((col * W, row * H, (col + 1) * W, (row + 1) * H))


def on_background(sprite, background, size=(W, H)):
    board = Image.new("RGBA", (W, H), background)
    board.alpha_composite(sprite)
    if size != (W, H):
        board = board.resize(size, Image.Resampling.LANCZOS)
    return board.convert("RGB")


def gif(frames, path, duration):
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=duration, loop=0, disposal=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, type=Path)
    parser.add_argument("--after", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    before = Image.open(args.before).convert("RGBA")
    after = Image.open(args.after).convert("RGBA")
    items = [("idle reference", cell(before, 0, 5)),
             ("wingbeat before", cell(before, 4, 4)),
             ("wingbeat after", cell(after, 4, 4))]

    for name, factor in (("native", 1), ("half", 0.5)):
        width, height = int(W * factor), int(H * factor)
        board = Image.new("RGB", (3 * width, 2 * (height + 18)), "white")
        draw = ImageDraw.Draw(board)
        for y, background in enumerate((LIGHT, DARK)):
            for x, (label, sprite) in enumerate(items):
                x0, y0 = x * width, y * (height + 18)
                draw.rectangle((x0, y0, x0 + width, y0 + height + 18), fill=background)
                draw.text((x0 + 3, y0 + 3), label, fill="black" if y == 0 else "white")
                board.paste(on_background(sprite, background, (width, height)), (x0, y0 + 18))
        board.save(args.output_dir / f"reference-before-after-{name}.png")

    # Five frames in order on light and dark backgrounds; each background has
    # a complete before row and after row so flicker and individual drift are visible.
    strip = Image.new("RGB", (W * 5, (H + 18) * 4), "white")
    draw = ImageDraw.Draw(strip)
    for y, (background, atlas, label) in enumerate(((LIGHT, before, "before"),
                                                    (LIGHT, after, "after"),
                                                    (DARK, before, "before"),
                                                    (DARK, after, "after"))):
        for x in range(5):
            x0, y0 = x * W, y * (H + 18)
            draw.rectangle((x0, y0, x0 + W, y0 + H + 18), fill=background)
            draw.text((x0 + 3, y0 + 3), f"{label} {x + 1}/5", fill="black" if y < 2 else "white")
            strip.paste(on_background(cell(atlas, 4, x), background), (x0, y0 + 18))
    strip.save(args.output_dir / "all-five-frames-before-after.png")

    for background, name in ((LIGHT, "light"), (DARK, "dark")):
        for atlas, stage in ((before, "before"), (after, "after")):
            wingbeat = [on_background(cell(atlas, 4, i), background) for i in range(5)]
            gif(wingbeat, args.output_dir / f"wingbeat-{stage}-{name}.gif", [240] * 5)
            idle = on_background(cell(atlas, 0, 5), background)
            gif([idle] * 3 + wingbeat + [idle] * 3,
                args.output_dir / f"idle-wingbeat-idle-{stage}-{name}.gif",
                [240] * 11)
    print(f"Color review artifacts written to {args.output_dir}")


if __name__ == "__main__":
    main()
