Create one horizontal animation strip for ChatGPT pet `gpt-chan`, state `idle`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure green #00FF00. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: User-approved silver-white long hair, lavender eyes, curved white dragon horns, pointed ears, white wings with lavender membranes, scaled long tail, high-collar white lavender draped dress with detached ruffled sleeves, asymmetric slit and long train, silver chains and knot rosettes; graceful 4.5-head proportions. Composed, capable, alert, lightly playful; preserve approved poses and no new props or quiet/expressive variants.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `auto`: Infer the most appropriate pet-safe style from the user request and reference images, then keep that exact style consistent across every row. User style notes: Approved polished anime sprite with crisp restrained linework, soft cool shading, simplified readable details at 192x208; no noisy ornament drift..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Calm low-distraction resting loop: subtle breathing, tiny blink, slight head/body bob, and only quiet persona-preserving motion.

State requirements:
- CRITICAL: idle is the low-distraction baseline state and the first frame is also used as the reduced-motion static pet.
- Use only subtle idle motion: gentle breathing, a tiny blink, a slight head or body bob, a very small material sway, or another quiet motion that fits the pet persona.
- Keep the pet essentially in the same pose, facing direction, silhouette, markings, palette, and prop state across all 6 frames.
- Idle variation must stay calm but still read as animation; do not repeat effectively identical copies across the loop.
- Do not show waving, walking, running, jumping, talking, working, reviewing, emotional reactions, large gestures, item interactions, or new props.
- Feet, base, body, or object anchor should remain planted or nearly planted.
- The first and last frames should be very close visually so the loop feels calm and does not pop.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.


Production clarification: output a VERY WIDE single row, exactly SIX complete figures, never two rows or a reference-sheet layout. Each figure must remain fully separated by generous pure green gutters. Keep all horn tips, wing tips, hands, shoes, train and tail visible. Maintain approved graceful proportions, not a squat redesign. Keep rosettes, silver chains and dress folds consistent. Frames 1-6: relaxed approved idle pose; a small inhale; eyelids lower; eyes close briefly for a calm blink; eyes reopen during exhale; nearly return to frame 1. No hand gesture changes, no speaking, no emotional reaction. All foot contacts and dress hem rest on one shared horizontal baseline. Subtle attached hair/tail motion, not whole-body size change. Render opaque background #00FF00, not transparency.
