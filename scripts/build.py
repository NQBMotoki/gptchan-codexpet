"""Validate registered v2 outfits, render documentation, and build a repeatable ZIP."""
import hashlib
import json
from pathlib import Path
import zipfile
import argparse
import copy
import os
import re

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PET = ROOT / "output" / "gpt-chan" if (ROOT / "output" / "gpt-chan").is_dir() else ROOT / "gpt-chan"
STATES = [("idle", 6), ("running-right", 8), ("running-left", 8),
          ("waving", 4), ("jumping", 5), ("failed", 8),
          ("waiting", 6), ("running", 6), ("review", 6)]


def validate(pet=PET):
    pet = Path(pet)
    from petctl import validate_pack
    validate_pack(pet)
    config = json.loads((pet / "pet.json").read_text(encoding="utf-8"))
    if config.get("id") != "gpt-chan" or config.get("spriteVersionNumber") != 2:
        raise ValueError("Expected gpt-chan native v2 configuration")
    if config.get("spritesheetPath") != "spritesheet.webp" or not config.get("displayName"):
        raise ValueError("Invalid sprite path or display name")
    with Image.open(pet / "spritesheet.webp") as source:
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
    from petctl import catalog, source_pack
    from preview import html
    destination = ROOT / "dist"
    destination.mkdir(exist_ok=True)
    archive = destination / "gptchan-codexpet.zip"
    info = copy.deepcopy(catalog(ROOT))
    if os.environ.get('GITHUB_REF_TYPE') == 'tag':
        version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
        if os.environ.get('GITHUB_REF_NAME') != 'v' + version:
            raise ValueError('Release tag must match VERSION exactly')
    files = {}
    for outfit, entry in info['outfits'].items():
        folder, metadata = source_pack(outfit, ROOT)
        validate(folder)
        prefix = 'gpt-chan' if outfit == info['defaultOutfit'] else f'outfits/{outfit}'
        entry['path'] = prefix
        for name in ('pet.json', 'spritesheet.webp'):
            files[f'{prefix}/{name}'] = (folder / name).read_bytes()
        files[f'{prefix}/NOTICE.md'] = (folder / 'NOTICE.md' if (folder / 'NOTICE.md').exists() else ROOT / 'NOTICE.md').read_bytes()
        files[f'{prefix}/release-info.json'] = (json.dumps(metadata, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    files['outfits.json'] = (json.dumps(info, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    files['preview.html'] = html(info).encode('utf-8')
    for name in ('VERSION', 'README.md', 'INSTALL.md', 'NOTICE.md', 'CHANGELOG.md', 'requirements.txt'):
        # Keep source-only gallery and concept links out of the distributable guide.
        files[name] = (ROOT / ('INSTALL.md' if name == 'README.md' else name)).read_bytes()
    for folder in ('scripts', 'docs'):
        for path in sorted((ROOT / folder).glob('*.py' if folder == 'scripts' else '*.md')):
            content = path.read_bytes()
            if folder == 'docs':
                # Artwork/production logs stay in the source checkout. Do not
                # leave clickable links to absent art/ files in the install ZIP.
                document = content.decode('utf-8')
                document = re.sub(r'!?\[([^\]]+)\]\(((?:\.\./)+art/[^)]+)\)',
                                  r'\1（制作素材位于源码仓库：\2）', document)
                content = document.encode('utf-8')
            files[path.relative_to(ROOT).as_posix()] = content
    for name in ('install.ps1', 'install.sh'):
        files[f'scripts/{name}'] = (ROOT / 'scripts' / name).read_bytes()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 14, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, content)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination / "SHA256SUMS.txt").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"Validated 9 animation states and 16 look directions. ZIP SHA256: {digest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-previews', action='store_true', help='Keep existing documentation images unchanged')
    args = parser.parse_args()
    from petctl import catalog
    from preview import html
    (ROOT / 'preview.html').write_text(html(catalog(ROOT)), encoding='utf-8')
    sheet = validate()
    if not args.no_previews:
        previews(sheet)
    package()
