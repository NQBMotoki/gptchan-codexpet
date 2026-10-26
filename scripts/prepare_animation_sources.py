"""Remove green matte from this white/lavender character's original strips.

Deterministic color keying only: no drawing, pose edits, or per-cell transforms.
Run on ORIGINAL generated strips before the bundled Pets extractor/despiller.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

STATES = ('idle', 'running-right', 'running-left', 'waving', 'jumping',
          'failed', 'waiting', 'running', 'review', 'look-row-9', 'look-row-10')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decoded-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--json-out', type=Path, required=True)
    args = parser.parse_args()
    if args.decoded_dir.resolve() == args.output_dir.resolve():
        parser.error('Keep original generated strips unchanged; use another output directory')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for state in STATES:
        source = args.decoded_dir / (state + '.png')
        with Image.open(source) as opened:
            image = opened.convert('RGBA')
        pixels = list(image.getdata())
        # No intentional green exists in the accepted white/lavender design.
        # RGB-distance keying alone misses shaded green inside wing/tail gaps.
        mask = [a > 0 and g > r + 30 and g > b + 30 for r, g, b, a in pixels]
        image.putdata([(0, 0, 0, 0) if keyed else pixel
                       for pixel, keyed in zip(pixels, mask)])
        destination = args.output_dir / source.name
        image.save(destination)
        records.append({'state': state, 'source': str(source.resolve()),
                        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                        'output': str(destination.resolve()),
                        'keyed_pixels': sum(mask)})
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps({
        'operation': 'background removal only, original source pixels',
        'rule': 'alpha > 0 and G > R + 30 and G > B + 30',
        'design_assumption': 'Accepted character has no green materials',
        'strips': records}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'prepared_strips': len(records)}))


if __name__ == '__main__':
    main()
