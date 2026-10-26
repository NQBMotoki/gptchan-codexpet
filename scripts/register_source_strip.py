"""Normalize an entire generated source canvas before bundled look registration.

One uniform transform for all eight poses and their spacing. Does not alter
individual poses, invent pixels, or replace the bundled extractor/compositor.
"""
import argparse
import json
import sys
from pathlib import Path
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tools-dir', type=Path, required=True)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--json-out', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.tools_dir.resolve()))
    from assemble_extended_atlas import extract_row_strip_cells
    reference = extract_row_strip_cells(args.reference, (0,255,0), 96)
    source = extract_row_strip_cells(args.source, (0,255,0), 96)
    heights = lambda cells: [cell.getbbox()[3]-cell.getbbox()[1] for cell in cells]
    reference_heights, source_heights = heights(reference), heights(source)
    for heights_in_row in (reference_heights, source_heights):
        if min(heights_in_row) < max(heights_in_row) * 0.65:
            raise ValueError('Pose groups are not eight complete comparable figures; keep source row rejected')
    factor = max(reference_heights) / max(source_heights)
    with Image.open(args.source) as opened:
        image = opened.convert('RGBA')
    size = (round(image.width * factor), round(image.height * factor))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.resize(size, Image.Resampling.LANCZOS).save(args.output)
    report = {'reference': str(args.reference.resolve()), 'source': str(args.source.resolve()),
              'output': str(args.output.resolve()), 'uniform_source_scale': factor,
              'reference_pose_heights': reference_heights, 'source_pose_heights': source_heights,
              'original_canvas': image.size, 'normalized_canvas': size,
              'per_pose_transforms': False, 'drawing_operations': False}
    args.json_out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
