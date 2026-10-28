# GPT酱 1.2.0-dev 素材生产记录

使用者选定 [03-compact-revision.png](../../samples/claude-style-study-20261027/03-compact-revision.png) 为角色外貌基准，并认可 [轻抚魔法阵的动作方向](references/approved-work-stroke.png)。参考图中的暖色服饰没有沿用。使用者指出一次 337.5° 修复稿的脸和眼睛过于圆润，该稿没有进入本图集。

## 保存的材料

- `sources/`：九种动作选用的生成源图，以及统一的十六向源图；左、右移动分别生成。源图是生成结果，不是直接安装的图集。
- `registered-frames/`：九状态共 57 个 192×208 已配准帧。每行使用固定尺度，跳跃源图的第二行统一作 11px 基线配准，以保留起落；没有逐帧非等比拉伸。
- `look-cells/`：从统一四行视线源图的透明间隔拆出的 16 个方向源格。组装时按同一比例及落地参考配准。
- `previews/`：从最终编码图集渲染的动作和视线预览，播放时间仅用于审看。
- `qa/`：结构、拆帧、方向连续性与透明行复核记录，以及原尺寸／半尺寸对照。图集验证记录与预览记录绑定最终哈希。

使用内置 imagegen 绘制源图，以绿色优势通道规则去除纯绿背景；经拆帧与配准组装后，对图集边缘进行一次去色，再编码透明无损 WebP。生成和中间图保留在本地；仓库保留选中的源图、配准帧及检查依据。生产工具来自 `work-pets` 0.1.6 的 create-pet 脚本；本地使用 Python 3.12.14 和 Pillow 12.3.0。

## 从已保存的配准帧重组

图集不需要重绘即可构建安装包；下列步骤只在需要核对制作过程时使用。将 `GPTCHAN_PET_SCRIPTS` 指向本机 `work-pets` 0.1.6 的 `create-pet/scripts` 目录，在仓库根目录运行：

```bash
GPTCHAN_TMP="$(mktemp -d)"
python "$GPTCHAN_PET_SCRIPTS/compose_atlas.py" \
  --frames-root art/animation/v1.2.0-dev/registered-frames \
  --output "$GPTCHAN_TMP/standard.png"
python "$GPTCHAN_PET_SCRIPTS/assemble_extended_atlas.py" \
  --base-atlas "$GPTCHAN_TMP/standard.png" \
  --look-cells-dir art/animation/v1.2.0-dev/look-cells \
  --output "$GPTCHAN_TMP/assembled.png"
python "$GPTCHAN_PET_SCRIPTS/despill_chroma_edges.py" "$GPTCHAN_TMP/assembled.png" \
  --output "$GPTCHAN_TMP/clean.png" --webp-output "$GPTCHAN_TMP/spritesheet.webp" \
  --chroma-key '#00FF00'
shasum -a 256 "$GPTCHAN_TMP/spritesheet.webp" output/gpt-chan/spritesheet.webp
```

在上述本地环境中重组后的哈希与安装图集一致：`1f1047c6999b6f05c80a7846f0b9143c835e704dbaed956d66e40299bbd9f330`。不同 Pillow／WebP 编码器版本不保证编码字节一致；若哈希不同，应同时检查解码像素与透明度。

## 验收边界

图集结构与隔离安装流程通过。两处视线相邻帧差异仍有自动警告；向下视线较窄，魔法阵在浅背景半尺寸下偏淡。真实宿主中的状态、鼠标跟随与播放效果由使用者实测，详见 [动画审看](../../../docs/ANIMATION-REVIEW-1.2.0-dev.md)。
