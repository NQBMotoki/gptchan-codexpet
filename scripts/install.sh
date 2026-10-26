#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_command="${GPTCHAN_PYTHON:-python3}"
if ! command -v "$python_command" >/dev/null 2>&1 || ! "$python_command" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
  echo 'Python 3.10+ is required for the verified installer. See INSTALL.md for manual installation.' >&2
  exit 1
fi
"$python_command" "$repo_dir/scripts/petctl.py" install "$@"
echo 'Local package verified. Reopen Codex and select GPT-chan; use doctor if the artwork is unchanged.'
