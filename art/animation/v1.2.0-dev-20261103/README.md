# GPT酱 1.2.0-dev.3：Candidate 08 注视组

使用者于 2026-11-03 审看 Candidate 08 的十六方向图与对比动图，确认可以使用并接受此前指出的小瑕疵。本版本无新绘制：将 `1.2.0-dev.2` 的九行动作与 Candidate 08 的两行注视原样组装。

- 基准图集 `1.2.0-dev.2` SHA-256：`41c8c08d51b1a59197263dfd5b8b1e6bbb221bd7c55b2d51d2be1f3cb3a6cf93`；它可从包含提交 `23436ebede107e3795d117c5c0f8d7654983dd79` 的 Git 克隆获取。
- 使用者确认的 Candidate 08 原图集 SHA-256：`b8a631f2bf052ed92187d330364b83edb341953796d5fb5897e15cd585d77040`；[已选两行](sources/approved-gaze-rows.png)的解码 RGBA SHA-256：`66988e74410af6141a059854e5824c6ada6dfd29042cd089d3eb3792b8979cb4`。
- 本版图集 SHA-256：`6756813298bf70fd7cf09e97b7f62e1e8bb88a34ced95c72b7cd0161e03ffea4`。九行动作逐字节比较解码 RGBA 与 dev.2 一致；注视两行与 Candidate 08 一致。
- `sources/look-row9-grid-03.png` 与 `sources/look-row10-grid-07.png` 是所选注视图的生成源，`sources/look-row9-registered-03.png` 是第一行配准中间件。`qa/` 保留盲测、原始连续性、结构检查与透明区域审看记录。

## 检查与审看

- 最终编码图集经 `validate_atlas.py` 和 Pets `validate_pet_spritesheet` 验证，尺寸为 1536×2288，11 行帧占用、透明背景和色键检查通过。 [结构报告](qa/atlas-validation.json) · [逐帧检查](qa/frame-inspection.json)
- [盲测](qa/blind-result-candidate-08.json)的四个主方向通过，部分中间方向有歧义提示；使用者审看后接受。保留 [方向审看记录](qa/direction-semantics-reviewed.json) 和 [原始连续性报告](qa/continuity-raw.json)。
- 连续性脚本把物体之间透明背景也标作疑似孔洞。此前对同一组注视帧做的四邻域检查和[标注图](qa/alpha-gap-visual-candidate-08.png)显示，突出标记位于翅膀与尾巴之间的负空间；原始提示没有删除。[审看数据](qa/alpha-gap-audit-candidate-08.json)
- 默认质量门禁因该动作没有 8 px 腾空而失败，符合使用者要求双脚基本着地的设计。使用 `--minimum-jump-lift 0` 复核后门禁通过但保留警告。两次实际报告分别为 [默认门禁](qa/quality-gate-default.json) 和 [着地设计门禁](qa/quality-gate-grounded.json)。
- [全动作动图](previews/all-states.gif) · [MP4](previews/all-states.mp4) · [注视循环](previews/look-loop.gif) · [待机→扇翼→待机](previews/idle-jump-idle.gif) · [四张衔接静帧](previews/jump-transition-stills.png) · [完整接触表](qa/contact-sheet.png)。预览速度只供审看，真实宿主效果由使用者验证。
- 本版素材、预览和检查记录已存入 ChatGPT 资料库的 `Pets / GPT酱`。云端原宠物已更新并回读校验，回读图片的解码 RGBA SHA-256 为 `afaaeb0cdce4e469b54f64cb07823f22ebaeff50823b2b6e19bb27445fd91780`，与本地图集一致；旧云端图集备份于本地 `dist/`。

## 重组图集

```bash
git show 23436ebede107e3795d117c5c0f8d7654983dd79:output/gpt-chan/spritesheet.webp > /tmp/gptchan-dev2-base.webp
python art/animation/v1.2.0-dev-20261103/rebuild_atlas.py \
  --base-atlas /tmp/gptchan-dev2-base.webp \
  --output /tmp/gptchan-dev3-rebuilt.webp
```

脚本校验 dev.2 文件哈希、已选注视 RGBA 像素、未修改动作与无损编码。不同 WebP 编码版本可能导致文件哈希不同，应比较解码后的 RGBA 像素。
