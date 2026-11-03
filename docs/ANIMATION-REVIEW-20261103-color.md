# GPT酱配色审看：1.2.0-dev.4

以待机配色为基准，按照使用者指定的数值调色方式调整五帧原地扇翼：紫色阴影更偏冷、饱和度更接近待机，皮肤轻微去饱和；没有生成或重画图像。其他八个动作、工作时魔法阵效果和 Candidate 08 的十六向注视与 dev.3 解码 RGBA 像素一致。

[原尺寸深浅背景对照](../art/animation/v1.2.0-dev4-color-20261103/previews/reference-before-after-native.png) · [半尺寸对照](../art/animation/v1.2.0-dev4-color-20261103/previews/reference-before-after-half.png) · [五帧对照](../art/animation/v1.2.0-dev4-color-20261103/previews/all-five-frames-before-after.png) · [待机→扇翼→待机](../art/animation/v1.2.0-dev4-color-20261103/previews/idle-wingbeat-idle-after-light.gif) · [所有动作](../art/animation/v1.2.0-dev4-color-20261103/previews/all-states/all-states.gif)

## 检查结果和边界

- 图集 1536×2288，原生 v2，九动作与十六向注视帧数、透明空格、色键残留检查通过；图集文件 SHA-256 为 `74cd3a5c85ba42fb64da74fe2b44cd5b84abb2ad0158409385f01e43516f4cbd`。
- 扇翼五帧仅改变颜色；整张图集 alpha 通道与 dev.3 完全一致。其余十行与跳跃行三个空格的解码 RGBA 完全一致。[数值报告](../art/animation/v1.2.0-dev4-color-20261103/qa/color-transform.json)
- 已对照头发、左翼、白裙、脸部皮肤和玫瑰饰品；原图和调色后使用同一组选中的像素进行比较。选区受姿势及材质混合影响，仅作辅证。[局部对照](../art/animation/v1.2.0-dev4-color-20261103/previews/material-crops.png) · [取样数据](../art/animation/v1.2.0-dev4-color-20261103/qa/material-samples.json)
- 复核所有动作后，左右移动的部分紫色阴影仍较深，但侧身和遮挡导致材质分布不同，未发现足以推翻已确认动作的同类明显偏粉，因此保留原像素。工作光效也保持原样。
- 自动质量检查按用户指定的着地扇翼使用 `--minimum-jump-lift 0`，其余注视方向和透明背景空隙保留 dev.3 已审看的提示；调色没有改变这些注视像素。[结构报告](../art/animation/v1.2.0-dev4-color-20261103/qa/atlas-validation.json) · [质量报告](../art/animation/v1.2.0-dev4-color-20261103/qa/quality-gate-grounded.json)
- GIF 每帧约 240 ms 的扇翼周期仅用于审看，真实宿主节奏、动作触发、鼠标跟随和显示效果由使用者验收。

原图、再现脚本、预览和检查过程见 [本次制作记录](../art/animation/v1.2.0-dev4-color-20261103/README.md)；dev.3 保留在其原位置。
