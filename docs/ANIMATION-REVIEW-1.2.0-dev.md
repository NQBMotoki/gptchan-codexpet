# GPT酱 1.2.0-dev 动画审看

本版本以使用者选定的 [根本形象](../art/samples/claude-style-study-20261027/03-compact-revision.png) 为依据，保留白龙娘的角色特征，并参考 Claude小姐的紧凑体型、待机节奏与像素感。工作时的手势来自此前认可的 [魔法阵动作参考](../art/animation/v1.2.0-dev/references/approved-work-stroke.png)；该旧图仅用于动作，不用于服饰配色。

[全部动作](../art/animation/v1.2.0-dev/previews/all-states.gif) · [十六向注视](../art/animation/v1.2.0-dev/previews/look-loop.gif) · [待机→跳跃→待机](../art/animation/v1.2.0-dev/previews/idle-jump-idle.gif) · [逐帧离线预览](../preview.html)

预览从本版本编码后的图集生成，GIF 的时间仅为审看设置。选用的源图、配准帧和制作说明保存在 [生产记录](../art/animation/v1.2.0-dev/PRODUCTION.md)。

## 已完成的离线检查

- 原生 v2：1536×2288，8×11 格；九个动作共 57 帧、16 个注视帧，其余 15 格透明。[结构检查](../art/animation/v1.2.0-dev/qa/atlas-validation.json)无错误或警告。
- 图集 SHA-256：`1f1047c6999b6f05c80a7846f0b9143c835e704dbaed956d66e40299bbd9f330`。
- 标准动作 [拆帧检查](../art/animation/v1.2.0-dev/qa/frame-inspection.json)无错误，九行均采用 stable-slots 并保留人工审看提示。原尺寸深色、半尺寸浅色及动作帧已审看；头饰保持在画面右侧。
- macOS 隔离环境打包及安装／备份／恢复等 11 项测试通过。具体环境及边界见 [兼容性记录](COMPATIBILITY.md)。

## 仍需在宿主中观察

[方向连续性检查](../art/animation/v1.2.0-dev/qa/direction-continuity.json)仍标记 067.5→090 和 157.5→180 两处相邻帧像素差偏大。检查同时对 16 个视线帧标记透明行；[边界泛洪复核](../art/animation/v1.2.0-dev/qa/alpha-gap-audit.json)显示这些标记行的透明区域与外部背景相连，没有发现封闭透明像素。该结论仅针对标记行，不替代整体视觉审看。

向下看时眼睛在小尺寸下较窄，可能像闭眼；魔法阵在半尺寸浅色背景上仍偏淡。真实桌面中的动作触发、播放速度、鼠标跟随、显示尺寸和资源刷新由使用者验证。本版本没有通过结构测试宣称这些行为已经通过。
