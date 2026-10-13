"""Validate the original v2 assets, render documentation, and build a repeatable ZIP."""
import hashlib
import json
from pathlib import Path
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PET = ROOT / "output" / "gpt-chan"
STATES = [("idle", 6), ("running-right", 8), ("running-left", 8),
          ("waving", 4), ("jumping", 5), ("failed", 8),
          ("waiting", 6), ("running", 6), ("review", 6)]


def validate():
    config = json.loads((PET / "pet.json").read_text(encoding="utf-8"))
    if config.get("id") != "gpt-chan" or config.get("spriteVersionNumber") != 2:
        raise ValueError("Expected gpt-chan native v2 configuration")
    if config.get("spritesheetPath") != "spritesheet.webp" or not config.get("displayName"):
        raise ValueError("Invalid sprite path or display name")
    with Image.open(PET / "spritesheet.webp") as source:
        if source.format != "WEBP" or source.mode != "RGBA" or source.size != (1536, 2288):
            raise ValueError("Expected 1536 x 2288 RGBA WebP")
        sheet = source.copy()
    if sheet.getchannel("A").getextrema() != (0, 255):
        raise ValueError("Expected transparent and opaque pixels")
    for row, count in enumerate([n for _, n in STATES] + [8, 8]):
        for col in range(8):
            occupied = frame(sheet, row, col).getchannel("A").getbbox() is not None
            if occupied != (col < count):
                raise ValueError(f"Unexpected occupied/blank cell: row {row}, col {col}")
    return sheet


def frame(sheet, row, col):
    return sheet.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))


def previews(sheet):
    destination = ROOT / "assets" / "readme"
    (destination / "animations").mkdir(parents=True, exist_ok=True)
    for row, (name, count) in enumerate(STATES):
        frames = [frame(sheet, row, col) for col in range(count)]
        frames[0].save(destination / f"{name}.png")
        # GIF previews use a neutral background to avoid palette transparency halos.
        gif_frames = []
        for cell in frames:
            background = Image.new("RGBA", cell.size, "#f4f0fa")
            background.alpha_composite(cell)
            gif_frames.append(background.convert("RGB"))
        gif_frames[0].save(destination / "animations" / f"{name}.gif",
                           save_all=True, append_images=gif_frames[1:],
                           duration=150, loop=0, disposal=2)


def package():
    destination = ROOT / "dist"
    destination.mkdir(exist_ok=True)
    archive = destination / "gptchan-codexpet.zip"
    files = {"gpt-chan/pet.json": PET / "pet.json",
             "gpt-chan/spritesheet.webp": PET / "spritesheet.webp",
             "gpt-chan/NOTICE.md": ROOT / "NOTICE.md"}
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, path in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 14, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination / "SHA256SUMS.txt").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"Validated 9 animation states and 16 look directions. ZIP SHA256: {digest}")


if __name__ == "__main__":
    previews(validate())
    package()
