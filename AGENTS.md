# GPT酱 Codex Pet project

## Scope and identity

This repository maintains the unofficial, AI-assisted GPT酱 desktop pet. The user selected `art/samples/claude-style-study-20261027/03-compact-revision.png` as the fundamental character reference. Preserve its white-haired, violet-eyed dragon-girl identity, white horns, pointed ears, white-and-lavender dress, wings, scaled tail, flower hair ornament, proportions, and restrained pixel-art feel. Older studies can inform actions but do not supersede this reference for appearance.

## Approved visual direction

- Idle should feel calm and restrained like the user's current Claude小姐 pet: stable stance, subtle motion and a natural blink. When her eyes are open in neutral idle, GPT酱 should look directly toward the user, with a natural, attentive expression.
- For the current style exploration, use the user-provided design sheet `art/samples/claude-style-study-20261027/user-design-reference.jpg` as the reference for GPT酱's appearance and cool white/silver/lavender accessories. The older waiting strip was accepted as a reference against reddish-copper drift, but the new sheet gives more specific appearance details. Do not claim the sheet's external authorship or authority is verified.
- Working uses a small white magic circle floating in front of her. One hand gently strokes or traces the circle as if sensing or shaping magic; the other supports it. The action is focused and evocative of gathering magic, without firing an attack. The user approved the direction in `art/animation/v1.2.0-dev/references/approved-work-stroke.png`.
- For other states, use the action's intent to decide gaze: greetings and user-facing waiting should visibly address the user when appropriate; looking at a magic circle, traveling in a direction, showing disappointment, or tracking the cursor may naturally require another direction. Keep eyes and face anatomically natural and expressions consistent with the state.
- Keep the flower ornament on the same anatomical side across frames. The user explicitly requires repair of the side-switching in the last four frames of the selected look strip; moving the flower while leaving its old tassels behind is incomplete.
- The user rejected the 2026-10-28 `look-337-grid.png` gaze repair because its rounder face and enlarged eyes drift from `03-compact-revision.png`. Do not include that source or the candidate assembled from it. Match the canonical face, eye shape, hair, proportions, costume details and restrained pixel rendering across every action; use regenerated material only after checking it against the canonical image.
- Preserve user-approved key poses and existing project assets. Save experiments separately; do not silently replace the current installation or publish a release. User approval of an art direction is not proof that every frame, transition or installation has passed validation.

## Production and validation

The native v2 atlas uses 192×208 cells, 8 columns and 11 rows: nine action rows with frame counts 6/8/8/4/5/8/6/6/6 and two full eight-frame rows for 16 gaze directions. Keep unused cells transparent. Check frame count, transparency, chroma fringes, character and ornament consistency, action continuity, grounded feet, jump motion and direction semantics. Review actual-size and half-size frames against light and dark backgrounds, plus transitions and animated loops. Record real limitations and distinguish automated structural checks from visual and in-app verification. Retain original generated source files and avoid overwriting prior candidates until the replacement has passed relevant checks.

The user selected the new reference for GPT酱 in a style closer to Claude小姐: less exaggerated chibi, less glossy and ornate, and more restrained pixel-sprite rendering. Her art style, motion, and proportions may be used as references; preserve GPT酱's distinct character design. See `art/samples/claude-style-study-20261027/README.md` and `art/animation/v1.2.0-dev/PRODUCTION.md`. Retain earlier assets. Preview GIF timing is illustrative unless verified in the host.

## Documentation

Keep `README.md` focused on the current project, installation, preview and maintenance. Record version-by-version changes in `CHANGELOG.md`; use `AGENTS.md` for enduring instructions for future work, not as a release history. Mark historical art and validation records clearly and keep their claims tied to the version and environment actually checked.
