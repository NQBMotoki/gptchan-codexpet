"""Register already-extracted AI frames across states; never draw or invent artwork.

The bundled Pets extractor preserves one transform within each row. This extra
geometry-only step gives those rows a common standing height and ground anchor.
The bundled inspector, compositor and final quality gates still run afterward.
"""
import argparse
import json
from pathlib import Path
import statistics

from PIL import Image

COUNTS = {'idle': 6, 'running-right': 8, 'running-left': 8, 'waving': 4,
          'jumping': 5, 'failed': 8, 'waiting': 6, 'running': 6, 'review': 6}


def bbox(image):
    return image.getchannel('A').point(lambda value: 255 if value > 16 else 0).getbbox()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frames-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--json-out', type=Path, required=True)
    parser.add_argument('--ground', type=int, default=202)
    args = parser.parse_args()
    source, destination = args.frames_root.resolve(), args.output_dir.resolve()
    if source == destination:
        raise ValueError('Preserve extracted originals; use a separate output directory')
    rows = {}
    for state, count in COUNTS.items():
        paths = sorted((source / state).glob('*.png'))
        if len(paths) != count:
            raise ValueError(f'{state}: expected {count} frames, found {len(paths)}')
        frames = [Image.open(p).convert('RGBA') for p in paths]
        boxes = [bbox(frame) for frame in frames]
        if any(frame.size != (192, 208) for frame in frames) or any(box is None for box in boxes):
            raise ValueError(f'{state}: expected complete extracted 192x208 frames')
        rows[state] = (frames, boxes)
    target_height = min(boxes[0][3] - boxes[0][1] for _, boxes in rows.values())
    manifest = json.loads((source / 'frames-manifest.json').read_text(encoding='utf-8'))
    reports = []
    for state, (frames, boxes) in rows.items():
        standing_height = boxes[0][3] - boxes[0][1]
        scale = target_height / standing_height
        # One matrix for the WHOLE row; jumping retains every vertical difference.
        ground = boxes[-1][3] if state == 'jumping' else statistics.median(box[3] for box in boxes)
        dimensions = (round(192 * scale), round(208 * scale))
        origin = (round((192 - dimensions[0]) / 2), round(args.ground - ground * scale))
        output = destination / state
        output.mkdir(parents=True, exist_ok=True)
        new_boxes = []
        for index, frame in enumerate(frames):
            resized = frame.resize(dimensions, Image.Resampling.LANCZOS)
            result = Image.new('RGBA', (192, 208))
            result.alpha_composite(resized, origin)
            new_box = bbox(result)
            if new_box is None or new_box[0] <= 1 or new_box[1] <= 1 or new_box[2] >= 191 or new_box[3] >= 207:
                raise ValueError(f'{state} {index}: registration would clip artwork')
            result.save(output / f'{index:02d}.png')
            new_boxes.append(new_box)
        reports.append({'state': state, 'scale': scale, 'origin': origin,
                        'source_standing_height': standing_height,
                        'source_boxes': boxes, 'registered_boxes': new_boxes})
    for row in manifest['rows']:
        row['frames'] = [str(destination / row['state'] / f'{i:02d}.png') for i in range(COUNTS[row['state']])]
    manifest['post_extraction_registration'] = str(args.json_out.resolve())
    (destination / 'frames-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    report = {'target_standing_height': target_height, 'ground': args.ground,
              'drawing_operations': False, 'one_transform_per_row': True, 'rows': reports}
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'registered_states': len(rows), 'target_standing_height': target_height}))


if __name__ == '__main__':
    main()
