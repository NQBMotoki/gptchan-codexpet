# GPT酱 · gpt-chan Codex Pet

GPT酱是一位白发紫瞳的白龙娘桌宠，穿着白紫礼服，带有龙角、龙翼与鳞尾。她有九种动作和十六向注视：待机时安静地看向你，工作时轻抚悬浮的白色魔法阵。

这是基于 [ZipZipPipe（B站 UID 4168597）](https://space.bilibili.com/4168597) 角色形象制作的非官方 AI 辅助二创，来源与权利说明见 [NOTICE.md](NOTICE.md)。

<table><tr>
<td align="center"><img src="assets/readme/animations/idle.gif" width="192" alt="GPT酱待机"><br>待机</td>
<td align="center"><img src="assets/readme/animations/running.gif" width="192" alt="GPT酱工作中"><br>工作</td>
<td align="center"><img src="assets/readme/animations/jumping.gif" width="192" alt="GPT酱跳跃"><br>跳跃</td>
</tr></table>

GIF 仅用于审看，播放速度和实际触发由宿主决定。

## 获取与安装

从 [Releases](https://github.com/NQBMotoki/gptchan-codexpet/releases) 下载正式版 ZIP，或克隆仓库使用主分支的开发版。主分支版本见 [VERSION](VERSION)，可能比最新正式版更新。

在仓库或解压目录运行：

```powershell
# Windows
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

```bash
# macOS / Linux
bash scripts/install.sh
```

脚本需要 Python 3.10+，仅使用标准库，不需要 Pillow、API Key 或网络。默认安装到 `CODEX_HOME/pets/gpt-chan/`；未设置 `CODEX_HOME` 时使用 `~/.codex`。安装程序会校验图集和哈希、备份原目录并在普通异常时恢复。安装后重新打开应用，在 Pets 设置中选择 GPT酱。

没有 Python 时也可以手动安装。完整步骤、备份与恢复方式见 [INSTALL.md](INSTALL.md) 和 [维护操作](docs/OPERATIONS.md)。

## 动作与预览

| 状态 | 用途 | 帧数 |
| --- | --- | --- |
| `idle` | 待机与眨眼 | 6 |
| `running-right` / `running-left` | 向右／向左移动 | 各 8 |
| `waving` | 挥手反馈 | 4 |
| `jumping` | 跳跃／完成 | 5 |
| `failed` | 失败反馈 | 8 |
| `waiting` | 等待确认 | 6 |
| `running` | 工作中的魔法阵动作 | 6 |
| `review` | 检查与思考 | 6 |

[全部动作预览](art/animation/v1.2.0-dev/previews/all-states.gif) · [十六向注视预览](art/animation/v1.2.0-dev/previews/look-loop.gif) · [逐帧离线预览](preview.html)

双击下载后的 `preview.html`，可以切换动作、逐帧查看、调整深浅背景和显示尺寸。图集为透明无损 WebP，尺寸 **1536 × 2288**，按 **8 × 11** 格排列，每格 **192 × 208**。第 9–10 行存放 16 个视线方向，未使用的格子透明。

角色基准与动作规范见 [形象基线](docs/ART-DIRECTION.md)，素材和检查结果见 [动画审看](docs/ANIMATION-REVIEW-1.2.0-dev.md)。半尺寸浅色背景下魔法阵较淡，视线有两处相邻帧差异警告；实际交互和桌面显示仍需在宿主中验收。

## 维护与验证

```bash
python scripts/petctl.py outfits
python scripts/petctl.py doctor
python scripts/petctl.py backups
python scripts/petctl.py restore BACKUP_ID
python scripts/petctl.py uninstall
```

命令可用 `--codex-home PATH` 指定目标。当前只有 `classic` 白紫礼服，服装登记与切换方法见 [换装说明](docs/OUTFITS.md)。本地工具不会自动切换账号云端宠物。

构建与隔离验证：

```bash
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/verify_install.py
```

构建验证图集并生成 `dist/gptchan-codexpet.zip` 和 `SHA256SUMS.txt`；使用 `--no-previews` 可保留现有 README 预览图。安装包包含手动安装目录、安装与维护脚本和更新日志。详细验证边界见 [兼容性记录](docs/COMPATIBILITY.md)，版本历史见 [CHANGELOG.md](CHANGELOG.md)。

## English

GPT-chan is an unofficial white dragon-girl pet based on a character design by ZipZipPipe. The native v2 atlas contains nine animation states and sixteen gaze directions.

Download a release or clone the repository, then run the Windows or macOS/Linux installer above. Installation requires Python 3.10+ and works offline. The local manager supports integrity checks, backups, restore and outfit selection; it does not change an account's cloud pet. See [INSTALL.md](INSTALL.md), [NOTICE.md](NOTICE.md), and [compatibility notes](docs/COMPATIBILITY.md).

## 贡献

修改前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。包结构参考 [remielle-codex-pet](https://github.com/HanaAyane/remielle-codex-pet)；本项目未使用该仓库的角色素材。
