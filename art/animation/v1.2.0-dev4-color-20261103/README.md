# GPT酱 1.2.0-dev.4：扇翼配色校正

2026-11-03，使用者要求以待机为基准统一九个动作的颜色，并选择“数值调色、先修明显偏差”，明确不生成新图像。本版本将原地扇翼的五帧从偏粉紫调整为较冷、较克制的紫色，轻微调整肤色；图像的动作、像素位置、透明度与轮廓未变。

- dev.3 基准图集：[已保留原图](../v1.2.0-dev-20261103/spritesheet.webp)，文件 SHA-256：`6756813298bf70fd7cf09e97b7f62e1e8bb88a34ced95c72b7cd0161e03ffea4`。
- dev.4 图集：[spritesheet.webp](spritesheet.webp)，文件 SHA-256：`74cd3a5c85ba42fb64da74fe2b44cd5b84abb2ad0158409385f01e43516f4cbd`；解码 RGBA SHA-256：`8288bf30e8c95bcee3302bea9b0282c812cca7cb4a45e0af2e3f12d16b5d4c16`。
- 同一条按颜色平滑加权的 HSV 曲线用于五帧；透明像素、alpha、动作其余八行、Candidate 08 十六向注视两行以及跳跃行的三个空格与基准逐字节一致。调色只作用于现有像素，无新增视觉素材。[数值变更报告](qa/color-transform.json)
- 原始绘制、去绿边与上一版本保持独立；源图及其许可说明继续沿用原有记录。

## 审看

[原尺寸深浅背景](previews/reference-before-after-native.png) · [半尺寸深浅背景](previews/reference-before-after-half.png) · [五帧前后对照](previews/all-five-frames-before-after.png) · [材质选区](previews/material-crops.png) · [材质样本](qa/material-samples.json)

[浅色背景扇翼循环](previews/wingbeat-after-light.gif) · [深色背景扇翼循环](previews/wingbeat-after-dark.gif) · [待机→扇翼→待机](previews/idle-wingbeat-idle-after-light.gif) · [所有动作 GIF](previews/all-states/all-states.gif) · [所有动作 MP4](previews/all-states/all-states.mp4) · [图集接触表](qa/contact-sheet.png)

用户截图最接近的两帧为待机第 6 帧与扇翼第 5 帧。后者在相同的原始紫色中间调选区内，饱和度中位数由 `0.2915` 调为 `0.2417`；待机对应筛选值约 `0.235`。两帧的姿态与材质占比不同，这不是标准色差或美术质量保证，仍需结合实际图像判断。

其他动作的原尺寸帧和接触表已审看：移动动作的部分阴影略浓，但侧身姿态与遮挡影响取样，未见足以推翻已认可素材的同类明显偏粉，因此保留原像素。工作魔法阵白紫光效保留。局部材质选区同样只能提供辅证。

最终编码图集通过 [原生 v2 结构与色键检查](qa/atlas-validation.json)、[逐帧检查](qa/frame-inspection.json)及使用 `--minimum-jump-lift 0` 的 [着地设计质量检查](qa/quality-gate-grounded.json)；另外经 Pets `validate_pet_spritesheet` 验证为有效。质量报告继续引用 dev.3 用户已接受的注视方向及连续性记录，且保留透明背景空隙和相邻注视帧差异提示。扇翼预览的每帧 240 ms 仅供审看，宿主播放、缩放和交互由使用者实际验收。

## 重建

仅依赖项目的 Pillow 环境。输出须指向新文件，避免覆盖原稿：

```bash
python art/animation/v1.2.0-dev4-color-20261103/recolor.py \
  --base-atlas art/animation/v1.2.0-dev-20261103/spritesheet.webp \
  --output /tmp/gptchan-dev4.webp \
  --frames-dir /tmp/gptchan-dev4-frames \
  --report /tmp/gptchan-dev4-color-report.json
```

脚本校验基准文件哈希、alpha、未修改行、空格和无损编码。不同版本的 WebP 编码器可能产生不同文件哈希；比较解码 RGBA 像素。
