# 安装 / Installation

脚本安装需要 Python 3.10+，只用标准库，无需 Pillow、API Key 或网络访问。没有 Python 时可按下方手动安装。

Windows：`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1`

macOS / Linux：`bash scripts/install.sh`

源码与解压后的 Release 使用相同命令。默认安装到 `CODEX_HOME/pets/gpt-chan/`；没有 CODEX_HOME 时使用用户目录 `.codex`。只操作这个本地宠物，不自动选择账号云端宠物。

手动安装：源码中的 `output/gpt-chan/`，或 Release 中的 `gpt-chan/`，包含 `pet.json` 和 `spritesheet.webp`。先备份原目录，再把整套文件及 NOTICE.md 复制到目标目录。手动方式不会执行脚本校验和自动恢复。

安装后重新打开应用，在 Pets 设置中选择 GPT酱。若显示未变，先运行 `python scripts/petctl.py doctor`，再确认当前显示是否来自账号云端副本。详见 [维护操作](docs/OPERATIONS.md)。

The verified installer requires Python 3.10+ and uses only its standard library. It runs offline and needs no API key. Use the Windows or Bash command above from a checkout or an extracted release. Existing packages are backed up outside the pet picker directory. Identical installs are skipped.

For manual installation without Python, copy pet.json, spritesheet.webp and attribution from output/gpt-chan (checkout) or gpt-chan (release) to CODEX_HOME/pets/gpt-chan, backing up the old folder first. Manual copying does not run installer checks. Local files do not prove that a selected cloud pet has changed.
