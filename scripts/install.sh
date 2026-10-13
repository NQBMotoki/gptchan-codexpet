#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_dir/output/gpt-chan"
codex_dir="${CODEX_HOME:-$HOME/.codex}"
target_dir="$codex_dir/pets/gpt-chan"
for filename in pet.json spritesheet.webp; do
  test -s "$source_dir/$filename" || { echo "Missing source: $filename" >&2; exit 1; }
done
mkdir -p "$codex_dir/pets"
if [[ -e "$target_dir" || -L "$target_dir" ]]; then
  backup_dir="$(mktemp -d "$codex_dir/pets/gpt-chan.backup.XXXXXXXX")"
  cp -R "$target_dir" "$backup_dir/original"
  echo "Backup: $backup_dir/original"
fi
mkdir -p "$target_dir"
cp "$source_dir/pet.json" "$source_dir/spritesheet.webp" "$target_dir/"
cmp "$source_dir/pet.json" "$target_dir/pet.json"
cmp "$source_dir/spritesheet.webp" "$target_dir/spritesheet.webp"
echo "Installed and verified: $target_dir"
echo "Reopen Codex and select GPT酱 in Settings → Pets."
