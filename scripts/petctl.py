"""Offline GPT-chan outfit/package manager. Python 3.10+, standard library only."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
PET_ID = 'gpt-chan'
FILES = ('pet.json', 'spritesheet.webp', 'NOTICE.md', 'release-info.json')
SLUG = re.compile(r'[a-z][a-z0-9-]{0,47}\Z')

def read_json(path):
    try:
        value = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    except (OSError, ValueError) as exc:
        raise ValueError(f'Cannot read JSON {path}: {exc}') from exc
    if not isinstance(value, dict):
        raise ValueError(f'Expected JSON object: {path}')
    return value

def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def child(root, relative):
    root = Path(root).resolve()
    value = Path(relative)
    if value.is_absolute() or '..' in value.parts or '\\' in str(relative):
        raise ValueError(f'Expected relative child path: {relative}')
    result = (root / value).resolve()
    if result == root or not result.is_relative_to(root):
        raise ValueError(f'Path leaves package root: {relative}')
    return result

def webp_size(path):
    """Validate RIFF/header boundaries, dimensions and alpha capability, not pixels."""
    data = Path(path).read_bytes()
    if len(data) < 20 or data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        raise ValueError('Expected WebP RIFF file')
    if int.from_bytes(data[4:8], 'little') + 8 != len(data):
        raise ValueError('Truncated or trailing WebP data')
    offset, sizes, alpha, images = 12, [], False, 0
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError('Truncated WebP chunk')
        kind = data[offset:offset + 4]
        length = int.from_bytes(data[offset + 4:offset + 8], 'little')
        payload = data[offset + 8:offset + 8 + length]
        offset += 8 + length + length % 2
        if len(payload) != length or offset > len(data):
            raise ValueError('Invalid WebP chunk length')
        if kind == b'VP8X':
            if len(payload) != 10 or payload[0] & 2:
                raise ValueError('Expected static WebP atlas')
            sizes.append((1 + int.from_bytes(payload[4:7], 'little'), 1 + int.from_bytes(payload[7:10], 'little')))
            alpha = alpha or bool(payload[0] & 16)
        elif kind == b'VP8L':
            if len(payload) < 5 or payload[0] != 47:
                raise ValueError('Invalid lossless WebP header')
            bits = int.from_bytes(payload[1:5], 'little')
            if bits >> 29:
                raise ValueError('Unsupported WebP version')
            sizes.append((1 + (bits & 16383), 1 + ((bits >> 14) & 16383)))
            alpha = alpha or bool((bits >> 28) & 1)
            images += 1
        elif kind == b'VP8 ':
            if len(payload) < 10 or payload[3:6] != b'\x9d\x01\x2a':
                raise ValueError('Invalid WebP bitstream header')
            sizes.append((int.from_bytes(payload[6:8], 'little') & 16383, int.from_bytes(payload[8:10], 'little') & 16383))
            images += 1
        elif kind == b'ALPH':
            alpha = True
        elif kind in (b'ANIM', b'ANMF'):
            raise ValueError('Animated WebP is not a sprite atlas')
    if images != 1 or not sizes or any(s != (1536, 2288) for s in sizes) or not alpha:
        raise ValueError('Expected alpha-capable 1536x2288 native v2 WebP')
    return sizes[0]

def validate_pack(folder, expected=None):
    folder = Path(folder).resolve()
    for name in ('pet.json', 'spritesheet.webp'):
        path = folder / name
        if path.is_symlink() or not path.is_file() or not path.stat().st_size:
            raise ValueError(f'Missing, empty or linked file: {path}')
    config = read_json(folder / 'pet.json')
    if config.get('id') != PET_ID or type(config.get('spriteVersionNumber')) is not int or config['spriteVersionNumber'] != 2:
        raise ValueError('Expected id=gpt-chan, spriteVersionNumber=2')
    if config.get('spritesheetPath') != 'spritesheet.webp' or not isinstance(config.get('displayName'), str) or not config['displayName'].strip():
        raise ValueError('Invalid displayName or spritesheetPath')
    webp_size(folder / 'spritesheet.webp')
    hashes = {name: sha256(folder / name) for name in ('pet.json', 'spritesheet.webp')}
    if expected is not None and hashes != expected:
        raise ValueError('Package hashes differ from catalog/release record; register intended artwork first')
    return config, hashes

def catalog(root=ROOT):
    value = read_json(Path(root) / 'outfits.json')
    if value.get('schemaVersion') != 1 or value.get('petId') != PET_ID or not isinstance(value.get('outfits'), dict):
        raise ValueError('Invalid outfit catalog')
    for key, entry in value['outfits'].items():
        if not SLUG.fullmatch(key) or not isinstance(entry, dict) or not entry.get('name'):
            raise ValueError('Invalid outfit ID/name')
        child(root, entry['path'])
    if value.get('defaultOutfit') not in value['outfits']:
        raise ValueError('Missing default outfit')
    return value

def provenance(root=ROOT):
    result = {'version': (Path(root) / 'VERSION').read_text(encoding='utf-8').strip()}
    try:
        result['sourceRevision'] = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL, text=True).strip()
        result['sourceDirty'] = bool(subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        result['sourceRevision'] = None
    return result

def source_pack(outfit=None, root=ROOT):
    info = catalog(root)
    outfit = outfit or info['defaultOutfit']
    if outfit not in info['outfits']:
        raise ValueError(f'Unknown outfit: {outfit}')
    entry = info['outfits'][outfit]
    folder = child(root, entry['path'])
    _, hashes = validate_pack(folder, entry.get('sha256', {}))
    if not (folder / 'NOTICE.md').is_file() and not (Path(root) / 'NOTICE.md').is_file():
        raise ValueError('Attribution NOTICE.md is required')
    metadata = {'schemaVersion': 1, 'petId': PET_ID, 'outfitId': outfit, 'outfitName': entry['name'],
                'spriteVersionNumber': 2, 'sha256': hashes, **provenance(root)}
    if (folder / 'release-info.json').is_file():
        saved = read_json(folder / 'release-info.json')
        if (saved.get('schemaVersion') != 1 or saved.get('sha256') != hashes
                or saved.get('outfitId') != outfit or saved.get('petId') != PET_ID
                or saved.get('spriteVersionNumber') != 2 or saved.get('version') != metadata['version']):
            raise ValueError('Invalid release-info.json')
        metadata = saved
    return folder, metadata

def home_path(value=None):
    return Path(value or os.environ.get('CODEX_HOME') or Path.home() / '.codex').expanduser().resolve()

def managed(home, relative):
    path = Path(home)
    for part in Path(relative).parts:
        path = path / part
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
            raise ValueError(f'Refusing linked managed path: {path}')
    return child(home, Path(relative).as_posix())

def remove_owned(path, parent):
    path, parent = Path(path), Path(parent).resolve()
    if path.is_symlink() or not path.resolve().is_relative_to(parent) or path.resolve() == parent:
        raise ValueError(f'Refusing cleanup outside managed root: {path}')
    shutil.rmtree(path)

@contextmanager
def operation(home):
    home.mkdir(parents=True, exist_ok=True)
    lock = home / '.gpt-chan.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError(f'Operation lock exists: {lock}; see docs/OPERATIONS.md') from exc
    os.close(fd)
    try:
        yield
    finally:
        lock.unlink()

def swap_pack(folder, home=None, metadata=None, common_notice=None):
    folder, home = Path(folder).resolve(), home_path(home)
    target = managed(home, 'pets/gpt-chan')
    staging_root = managed(home, '.pet-staging')
    backups = managed(home, '.pet-backups/gpt-chan')
    with operation(home):
        staging_root.mkdir(parents=True, exist_ok=True)
        stage = staging_root / f'gpt-chan-{uuid.uuid4().hex}'
        stage.mkdir()
        backup = None
        try:
            for name in FILES:
                source = folder / name
                if name == 'NOTICE.md' and not source.is_file() and common_notice:
                    source = Path(common_notice)
                if source.is_file():
                    if source.is_symlink():
                        raise ValueError(f'Refusing linked package file: {source}')
                    shutil.copy2(source, stage / name)
            if metadata:
                write_json(stage / 'release-info.json', metadata)
            _, hashes = validate_pack(stage, metadata['sha256'] if metadata else None)
            if metadata and target.is_dir() and all((target / n).is_file() and (target / n).read_bytes() == (stage / n).read_bytes() for n in FILES):
                return {'status': 'unchanged', 'target': str(target), 'outfitId': metadata['outfitId']}
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if not target.is_dir():
                    raise ValueError('Installed path is not a directory')
                backups.mkdir(parents=True, exist_ok=True)
                backup = backups / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:12])
                target.rename(backup)
            try:
                stage.rename(target)
                validate_pack(target, hashes)
            except BaseException:
                if target.exists():
                    remove_owned(target, target.parent)
                if backup:
                    backup.rename(target)
                raise
            return {'status': 'installed', 'target': str(target), 'backup': str(backup) if backup else None,
                    'version': metadata.get('version') if metadata else None, 'outfitId': metadata.get('outfitId') if metadata else None}
        finally:
            if stage.exists():
                remove_owned(stage, staging_root)

def install(outfit=None, home=None, root=ROOT):
    folder, metadata = source_pack(outfit, root)
    return swap_pack(folder, home, metadata, Path(root) / 'NOTICE.md')

def backup_list(home=None):
    parent = managed(home_path(home), '.pet-backups/gpt-chan')
    return sorted((p.name for p in parent.iterdir() if p.is_dir() and not p.is_symlink()), reverse=True) if parent.exists() else []

def restore(backup_id, home=None):
    if not re.fullmatch(r'[0-9]{8}T[0-9]{6}Z-[a-f0-9]{12}', backup_id):
        raise ValueError('Use an exact backup ID from backups command')
    home = home_path(home)
    folder = managed(home, f'.pet-backups/gpt-chan/{backup_id}')
    _, hashes = validate_pack(folder)
    metadata = read_json(folder / 'release-info.json') if (folder / 'release-info.json').exists() else None
    if metadata and metadata.get('sha256') != hashes:
        raise ValueError('Backup integrity check failed')
    return swap_pack(folder, home, metadata)

def uninstall(home=None):
    home = home_path(home)
    target = managed(home, 'pets/gpt-chan')
    with operation(home):
        if not target.exists():
            return {'status': 'not-installed'}
        backups = managed(home, '.pet-backups/gpt-chan')
        backups.mkdir(parents=True, exist_ok=True)
        destination = backups / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:12])
        target.rename(destination)
        return {'status': 'uninstalled', 'backup': str(destination)}

def doctor(home=None, root=ROOT):
    home = home_path(home)
    target = managed(home, 'pets/gpt-chan')
    result = {'codexHome': str(home), 'target': str(target), 'installed': target.is_dir(),
              'activeDisplaySource': 'unverified: local inspection cannot identify the active cloud pet',
              'lockPresent': (home / '.gpt-chan.lock').exists(), 'backups': backup_list(home)}
    if result['installed']:
        try:
            _, hashes = validate_pack(target)
            result.update(validation='header-and-manifest-valid', sha256=hashes)
            if (target / 'release-info.json').exists():
                saved = read_json(target / 'release-info.json')
                result.update(releaseInfo=saved, integrityMatchesRecord=hashes == saved.get('sha256'))
            else:
                result['releaseInfo'] = 'unknown: legacy/manual package'
            result['matchesAvailableOutfits'] = [k for k, e in catalog(root)['outfits'].items() if e.get('sha256') == hashes]
        except (OSError, ValueError) as exc:
            result.update(validation='invalid', error=str(exc))
    return result

def import_outfit(outfit, source, name, root=ROOT):
    if not SLUG.fullmatch(outfit) or not name.strip():
        raise ValueError('Use a lowercase outfit ID and a nonempty name')
    info = catalog(root)
    if outfit in info['outfits']:
        raise ValueError('Outfit already exists; use a new versioned ID')
    source = Path(source).resolve()
    _, hashes = validate_pack(source)
    if not (source / 'NOTICE.md').is_file():
        raise ValueError('New outfits must include NOTICE.md')
    from build import validate
    validate(source)
    destination = child(root, f'outfits/{outfit}')
    if destination.exists():
        raise ValueError('Outfit destination already exists')
    destination.mkdir(parents=True)
    try:
        for filename in ('pet.json', 'spritesheet.webp', 'NOTICE.md'):
            shutil.copy2(source / filename, destination / filename)
        validate_pack(destination, hashes)
        info['outfits'][outfit] = {'name': name, 'path': f'outfits/{outfit}', 'sha256': hashes}
        temporary = Path(root) / f'.outfits-{uuid.uuid4().hex}.json'
        try:
            write_json(temporary, info)
            os.replace(temporary, Path(root) / 'outfits.json')
        finally:
            temporary.unlink(missing_ok=True)
    except BaseException:
        remove_owned(destination, Path(root) / 'outfits')
        raise
    return {'status': 'registered', 'outfitId': outfit, 'path': str(destination)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('install', 'doctor', 'backups', 'restore', 'uninstall'):
        p = sub.add_parser(command)
        p.add_argument('--codex-home')
        if command == 'install':
            p.add_argument('--outfit')
        if command == 'restore':
            p.add_argument('backup_id')
    sub.add_parser('outfits')
    p = sub.add_parser('import-outfit')
    p.add_argument('outfit_id')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--name', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'install':
            value = install(args.outfit, args.codex_home)
        elif args.command == 'doctor':
            value = doctor(args.codex_home)
        elif args.command == 'backups':
            value = {'backups': backup_list(args.codex_home)}
        elif args.command == 'restore':
            value = restore(args.backup_id, args.codex_home)
        elif args.command == 'uninstall':
            value = uninstall(args.codex_home)
        elif args.command == 'outfits':
            value = catalog()
        else:
            value = import_outfit(args.outfit_id, args.source, args.name)
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return 2 if args.command == 'doctor' and (value.get('validation') == 'invalid' or value.get('integrityMatchesRecord') is False) else 0
    except (OSError, ValueError, KeyError, ImportError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
