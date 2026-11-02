# 2026-11-02 工作与跳跃动画

`1.2.0-dev.1` 在既有 `1.2.0-dev` 图集上更新两行：工作时魔法阵自身散发白紫光效；跳跃时双翼随起落上抬、回落。角色仍以[根本形象](../../samples/claude-style-study-20261027/03-compact-revision.png)为准，工作特效方向见[已认可的样稿](../../samples/work-vfx-study-20261101/)。

`sources/` 保存内置 imagegen 生成的原始绿底图，`registered-frames/` 保存最终两行动作帧，`previews/` 和 `qa/` 来自下方图集。完整提示词见 [PROMPTS.md](PROMPTS.md)。2026-10-28 的图集和素材记录仍可通过[原生产记录](../v1.2.0-dev/PRODUCTION.md)及 Git 历史查看。

## 制作与验证

- 原始 3×2 网格按格子顺序无重绘地重排，使用既有绿幕去除规则和 `work-pets` 0.1.6 的 `extract_strip_frames.py`，以 `stable-slots` 提取 5 张跳跃帧与 6 张工作帧。
- 两个动作分别使用统一缩放。跳跃源图上、下两行只做各自统一的垂直配准，以维持起跳高度及落地基线；工作帧使用同一配准。随后对透明边缘去色。实际参数与边界见 `qa/registration.json`。
- 在旧图集上仅替换跳跃与工作格；其余九行以及这两行的空白格保持原像素。无损编码、尺寸、透明度、空格及绿色边缘通过检查。跳跃帧最小留白为 3 px。
- `stable-slots` 提取保留两项人工审看提示；全尺寸与半尺寸、深色与浅色背景的静态对照见 `qa/light-dark-sizes.png`。浅色半尺寸时魔法阵细线仍较淡。
- GIF 时间仅供审看。动作触发、实际播放节奏、真实桌面缩放及鼠标交互尚未在宿主中验收，由使用者测试。

旧图集 SHA-256：`1f1047c6999b6f05c80a7846f0b9143c835e704dbaed956d66e40299bbd9f330`。当前图集 SHA-256：`b3a521ed88820aa4d5aa2d7bf70f003fbcec6c7ea36f398f4a5f0abdfd3307aa`。

## 从保留的帧重建

从包含提交 `766758b03f593ab6e52db35b2bdb2db91adeea2f` 的 Git 克隆中提取旧图集，再用 Pillow 运行本目录的脚本：

```bash
git show 766758b03f593ab6e52db35b2bdb2db91adeea2f:output/gpt-chan/spritesheet.webp > /tmp/gptchan-base-20261028.webp
python art/animation/v1.2.0-dev-20261102/rebuild_atlas.py \
  --base-atlas /tmp/gptchan-base-20261028.webp \
  --output /tmp/gptchan-rebuilt-20261102.webp
```

脚本拒绝覆盖输出，校验旧图集哈希，检查未修改的行并确认 WebP 解码像素无损。本机 Python 3.12 / Pillow 13.0.0 重建后哈希与当前图集一致；不同编码器版本应比较解码后的像素。
