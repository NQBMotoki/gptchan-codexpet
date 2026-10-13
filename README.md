# GPT酱 · gpt-chan Codex Pet

白发紫瞳、神态疏淡的 GPT 龙娘，穿着白紫长裙，带有龙角、龙翼与龙尾。微像素动漫画风，适用于支持原生 v2 桌宠的 Codex Desktop。

原形象作者：**[ZipzipPipe（B站 UID 4168597）](https://space.bilibili.com/4168597)**。本项目为非官方 AI 辅助二创，来源与权利说明见 [NOTICE.md](NOTICE.md)。

<table>
<tr>
<td align="center"><img src="assets/readme/animations/idle.gif" width="192" alt="GPT酱待机"><br>待机</td>
<td align="center"><img src="assets/readme/animations/running.gif" width="192" alt="GPT酱工作中"><br>工作中</td>
<td align="center"><img src="assets/readme/animations/jumping.gif" width="192" alt="GPT酱完成庆祝"><br>完成庆祝</td>
</tr>
</table>

## 快速安装

原生安装只需将 [`output/gpt-chan/pet.json`](output/gpt-chan/pet.json) 与 [`output/gpt-chan/spritesheet.webp`](output/gpt-chan/spritesheet.webp) 放在同一个 `gpt-chan` 文件夹中。安装脚本会先备份已有的同名文件，随后复制两个文件；不会操作其他桌宠。

### Windows（PowerShell）

```powershell
git clone https://github.com/NQBMotoki/gptchan-codexpet.git
Set-Location gptchan-codexpet
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

默认安装路径：`%USERPROFILE%\.codex\pets\gpt-chan\`。

### macOS

```bash
git clone https://github.com/NQBMotoki/gptchan-codexpet.git
cd gptchan-codexpet
bash scripts/install.sh
```

默认安装路径：`~/.codex/pets/gpt-chan/`。两个安装脚本均尊重已有的 `CODEX_HOME` 设置。

### 手动安装

从本仓库的 **Code → Download ZIP** 下载源码并解压。创建上述安装目录，把 `output/gpt-chan/` 中的 `pet.json` 和 `spritesheet.webp` 复制进去。已有同名文件时请先备份。

重新启动 Codex，在 **设置 → Pets** 中刷新列表并选择 **GPT酱**。仓库配置并不会自动安装到你的电脑。

### Agent 安装提示词

```text
请在这台电脑上安装 https://github.com/NQBMotoki/gptchan-codexpet 的 GPT酱桌宠。
读取仓库 README，识别操作系统，下载 output/gpt-chan/pet.json 和 spritesheet.webp。
使用 CODEX_HOME（若已设置），否则使用用户目录中的 .codex，安装到 pets/gpt-chan/。
已有同名文件时先备份，不操作其他桌宠。检查 id 为 gpt-chan、spriteVersionNumber 为 2，
图集为 1536×2288 透明 WebP。报告实际路径，并提醒我重启 Codex，在设置 → Pets 中选择 GPT酱。
若无法显示，先诊断版本和运行后端，不要擅自修改后端设置或转换图集格式。
```

## 动作图鉴

| 预览 | 原生状态 | 语义 | 图集行（从 0 开始） | 帧数 |
| --- | --- | --- | --- | --- |
| ![待机](assets/readme/idle.png) | `idle` | 待机 | 0 | 6 |
| ![向右移动](assets/readme/running-right.png) | `running-right` | 向右移动 | 1 | 8 |
| ![向左移动](assets/readme/running-left.png) | `running-left` | 向左移动 | 2 | 8 |
| ![挥手](assets/readme/waving.png) | `waving` | 互动反馈 | 3 | 4 |
| ![完成庆祝](assets/readme/jumping.png) | `jumping` | 跳跃／完成庆祝 | 4 | 5 |
| ![失败](assets/readme/failed.png) | `failed` | 失败 | 5 | 8 |
| ![等待](assets/readme/waiting.png) | `waiting` | 等待确认 | 6 | 6 |
| ![工作中](assets/readme/running.png) | `running` | 工作中 | 7 | 6 |
| ![检查中](assets/readme/review.png) | `review` | 检查中 | 8 | 6 |

第 9–10 行包含 16 向视线，每行 8 格。各格尺寸为 **192 × 208**，整张图集为 **1536 × 2288**、8 列 × 11 行的透明无损 WebP。GIF 用于文档预览，播放速度不代表 Codex 运行器的实际速度。

<details><summary>完整精灵图集</summary>

![GPT酱 v2 精灵图集](output/gpt-chan/spritesheet.webp)

</details>

## 验证与打包

```bash
python -m pip install -r requirements.txt
python scripts/build.py
```

脚本检查配置、尺寸、透明度、有效帧和空白格，生成 PNG／GIF 预览，并输出 `dist/gptchan-codexpet.zip`。解压后得到 `gpt-chan/pet.json`、`gpt-chan/spritesheet.webp` 与来源声明。GitHub Actions 也会执行相同检查并提供 ZIP artifact；当前未发布 Release。

## 项目结构

- `output/gpt-chan/`：原生 v2 安装包。
- `assets/readme/`：九个动作的 PNG 与 GIF 预览。
- `scripts/`：验证、打包和 Windows／macOS 安装脚本。
- `.github/workflows/package.yml`：自动验证与打包。
- `NOTICE.md`：素材来源与署名。

## 已知限制

动作触发、鼠标视线跟随由 Codex 运行器决定，本仓库不提供事件监听程序。安装后无法显示时，请先确认两个文件的位置、Codex 版本与实际使用的 `CODEX_HOME`。Windows 使用 WSL 后端时可参考上游兼容性问题 [openai/codex#20730](https://github.com/openai/codex/issues/20730)；修改后端可能影响工作流，应由使用者决定。

包结构参考 [remielle-codex-pet](https://github.com/HanaAyane/remielle-codex-pet)，使用的是仓库所有者现有 GPT酱素材。
