# 工作形态：魔法阵发光特效样稿

本目录是 2026-11-01 的未定稿视觉探索，没有替换宠物图集或本机安装。

- `01-magic-circle-effect-concept.png`：单幅效果示意，重点审看阵面光晕和向上流动的光；人物细节不作为新的形象基准。
- `02-work-state-effect-study.png`：把相同方向放回六格工作动作的概念图，仅供审看，并非可直接播放的动画或成品帧。

人物与动作仍以 `art/samples/claude-style-study-20261027/03-compact-revision.png` 和 `art/animation/v1.2.0-dev/sources/work-canonical-gesture.png` 为准。正式应用前需要依照用户反馈制作连续帧，并检查桌宠尺寸和浅色背景下的可见性。

使用 Codex 内置 imagegen 生成；参考图中，第 1 张为编辑目标，第 2、3 张按各提示词说明作为角色或效果参考。

## 单幅效果提示词

参考：先前六格特效草稿、角色根本形象、现有工作动作。

```text
Use case: precise-object-edit. Create ONE large full-body concept illustration of the existing GPT-chan work pose from image 3, not a six-frame sheet. Preserve the visual identity and proportions in image 2 and the white-and-lavender character and pose of image 1. Design brief: the floating white magic circle BETWEEN HER TWO HANDS ITSELF EMITS CLEARLY VISIBLE MAGICAL ENERGY. This is the focal point. Draw the circle as a delicate horizontal ellipse, with bright white fine concentric glyph rings and pale-violet edging, about the width of her torso. FROM THE RING'S SURFACE AND OUTER EDGE, render three distinct short upward-flowing white-lavender ribbons of light, clearly connected at their bases to the circle; small glowing geometric flecks rise directly off the ring between those ribbons and fade a short distance above it; delicate translucent expanding light-ripples originate at the top hand's fingertip on the circle. A compact diffuse halo hugs the outer edge of the ring, making it visibly shine. The small ribbon emission should read immediately as a magic circle radiating effects, not isolated decorative stars. Keep all emitted effects close to her hands and torso, subtle enough not to cover her face or body, yet clearly visible in this concept. Hands: her upper hand gently brushes and manipulates the circle; lower hand open and supporting it from below. Her gaze is calm and focused on the circle. She is shaping and sensing magic, not attacking. No independent sparkles around her wings or tail, no explosion, no weapon, no book, no beam firing outward, no magic circle on the ground. Exact identity: silver-white long wavy hair, violet eyes, white ivory curved horns, pointed ears, white rose headpiece with tassel on viewer-right, delicate white dress with silver and lavender ornaments, violet crystals, batlike wings, scaled lavender tail, face and body proportions faithful to image 2. Preserve a restrained lightly pixelated sprite-art feel, do not make face rounder or eyes larger. A uniform dark desaturated plum background, no scenery, no text, labels, watermark or border. Full body, uncut horns, wings, skirt and tail.
```

## 六格动作示意提示词

参考：现有工作动作、上面的单幅特效示意、角色根本形象。

```text
Use case: precise-object-edit. Image 1 is the exact source to edit. KEEP ALL SIX full-body characters, their original 3-column by 2-row arrangement, sizes, proportions, faces, poses, hands, skin, costumes, horns, hair, white rose on viewer-right, wings, and tails as nearly IDENTICAL to image 1 as possible. Image 3 is the absolute character appearance reference. Do not redraw, beautify, recolor or redesign the characters. Change only the magical visual effects on and close to the small floating circle held between her hands; and replace green backing with plain muted dark charcoal-plum for this draft presentation. Use image 2 ONLY as reference for the type of magic being emitted, not character styling or proportions: bright white/pale-lavender fine concentric ring lines, a compact luminous halo around the actual ring, a visible fine curved rising wisp anchored to the circle's rim, and two or three tiny flecks that emerge directly from the ring and gently fade upward. The emitter is the circle itself; these visible effects must be rooted at the array and stay within a circle-radius of it. The top hand is gently brushing the luminous surface, lower hand supports the array, magic gathers and pulses without firing. Across the six existing panels vary the brightness and wisp positions smoothly in small steps to suggest one subtle animation loop. Keep the circle and its emission legible at 192x208 and prevent the effects from covering her face, dress or hands. Preserve muted white, silver and lavender palette and restrained pixel-sprite detail from image 1. No unattached sparkles by wings or tail, no books, weapons, projectiles, attacks, explosions, additional figures, scenery, text, labels, borders or watermarks. No face or costume changes. All horns, wings, feet, and tails remain visible.
```
