# Independent final encoded-atlas visual review — repaired revision

Reviewed: 2026-10-27. Scope: independent visual review of the exact encoded `final/spritesheet.webp`. No artwork modification, upload, activation, or cloud verification was performed.

## Verdict

**Visual pass at native pet size, with minor first-version limitations and trace color-tint warnings. No remaining hard visual defect was observed in this repaired revision.** The prior bright enclosed green patches have substantially cleared, and the prior look-family body-proportion step has been corrected. This is not a claim of zero green-valued pixels, perfect subpixel edges, real-time playback acceptance, or successful completion of every other mandatory final gate.

The preceding failed review is preserved separately as `final-independent-review-key160.md`; its findings refer to the earlier hash, not these repaired bytes.

## Exact artifact and method

- Artifact: `final/spritesheet.webp`, 1536 x 2288, 192 x 208 cells.
- SHA-256: `87e703010439e620479566b674a1bafa84542fd6f92387faf791600709d08111`.
- Fresh Pillow decode of these exact bytes; all **57 standard frames and all 16 look cells** were cropped directly from this WEBP and examined in order at native cell size on both `#f0eef6` and `#171923` backgrounds.
- Deterministic diagnostic crops are saved in `qa/final-independent-evidence-repaired/`. They do not alter the atlas. `row-00.png` through `row-10.png` contain every used cell in both backgrounds; each sprite occupies its original 192 x 208 pixels.
- A 2x nearest-neighbor color-detail sheet and a seam landmark-grid sheet were also inspected. Magnification supports diagnosis; native-size visibility determines whether a subtle issue is a material visual defect.
- No blind answer keys, blind verdicts, other reviewers' answer records, or generation prompts were read. The implementation metadata `look-source-registration.json` was read after the images: it records one uniform source-canvas scale of 0.9558541266794626, no per-pose transforms and no drawing operations. This report independently assesses the output rather than assuming that the stated correction passed.
- Ordered frames were inspected. No claim is made to have watched real-time playback.

## Recheck of the earlier failures

### Green remnants: blocking patches resolved; minor traces remain

The earlier opaque, bright green clusters in running hair are no longer visible as coherent bright islands at native size. The fine hair remains readable; I did not observe a new hole through the body, a missing major strand mass, or a clipped wing caused by this repair.

Former failure sample locations now have greatly reduced opacity:

| Cell, local coordinate | Repaired RGBA | Observation |
| --- | --- | --- |
| running-right00 (92,82) | (74,156,74,31) | Former fully opaque pale-green patch is now faint and largely transparent. |
| running-right00 (91,82) | (0,145,0,7) | Negligible-alpha remnant rather than the old solid island. |
| running-right04 (73,111) | (183,203,197,19) | Very low-alpha pale edge remnant. |
| running-right04 (88,87) | (39,137,0,13) | Low-alpha remnant. |
| running-left04 (97,105) | (61,128,86,91) | Reduced to a small translucent tint among hair strands. |
| running-left04 (113,80) | (114,133,138,42) | Low-alpha near-gray remnant. |

This does **not** mean the final has absolutely no residual green bias. Pixel inspection and the 2x diagnostic still reveal a few muted gray-green microdots and translucent edge tints. Examples include running-left03 (92,88) = (58,104,72,214) and running-left04 (89,94) = (56,98,64,195). These are isolated dark microdetails, not the earlier solid bright patches. In the complete native-size light/dark review they did not form a distracting green panel, halo, or obvious interior blotch.

For transparency about the diagnostic: a deliberately sensitive check using alpha >=160 and G-max(R,B)>=8 still finds 15/18/13 candidate pixels in running-right00/running-right04/running-left04. The largest 4-connected candidate group across the atlas has 6 pixels; two pixels exceed a 30-channel green-dominance threshold. These values are supplementary evidence, not a replacement for visual judgment. A trace-tint warning remains; I do not classify the observed native-size result as the former hard chroma defect.

Evidence: `row-01.png`, `row-02.png`, and `color-detail-2x.png` in the repaired evidence directory.

### Look-family proportion step: resolved at waist, hip and ankle landmarks

The source-family correction visibly reduces the previous longitudinal body mismatch. The foot baseline remains fixed and the waist/hip/thigh landmarks now agree closely enough for the remaining head displacement to read as a pose/gaze change.

Approximate manually read landmark coordinates, with about +/-2px uncertainty:

| Landmark | 157.5 r9/f7 | 180 r10/f0 | 337.5 r10/f7 | 000 r9/f0 |
| --- | ---: | ---: | ---: | ---: |
| Waist/hip flower center | y112 | y110 | y110 | y112 |
| Upper vertex of exposed-thigh/dress opening | y127 | y125 | y125 | y128 |
| Ankle ornament/cuff | about y182 | about y181-182 | about y181-182 | about y182 |
| Visible bottom, exact alpha bbox | y202 | y202 | y202 | y202 |
| Visible top, exact alpha bbox | y41 | y35 | y33 | y36 |

- **157.5 -> 180:** the face changes from down-right to frontal-down. The residual top difference is6px, while waist/hip differences are around2px and the ankles/feet remain stable. Chin, hair and horn silhouette naturally change with the head turn and pitch. I no longer observe the earlier whole upper-body lengthening step.
- **337.5 -> 000:** the up-left profile returns toward front-up. Top difference is3px, the waist differs about2px and the ankles/feet remain stable. This reads as a normal face/neck pose change rather than a family scale jump.
- **292.5 -> 315:** both repaired tops are y33 and bottoms y202. The head pitches more strongly upward; the waist, exposed thigh and ankle stay coherent. No hard registration or identity defect is observed.

The exact visible-top values are provided for context, not used alone as a scale test. Head dimensions cannot be compared independently with precision across changing yaw/pitch; I do not assert an isolated head-size change.

Evidence: repaired `row-09.png`, `row-10.png`, `seams-landmark-grid-2x.png`. The grid sheet is diagnostic magnification; native cells in the row sheets were also inspected.

## All standard animation rows

| Row/state | Frames inspected | Result and evidence |
| --- | --- | --- |
| 0 idle | 00-05 | Calm blink and micro-variation; eyes and identity remain readable; no inert repeated still. Standing bottom204 throughout. |
| 1 running-right | 00-07 | Correct screen-right face; open strides00/04 and gathered legs01/05 establish cadence, hair and skirt trail left. No reversal observed. Trace tint warning above remains. |
| 2 running-left | 00-07 | Correct screen-left face; changing stride and hair/skirt drag right. No wrong-direction or temporal reversal observed. Trace tint warning above remains. |
| 3 waving | 00-03 | Attached raised/open hand in01/02, returning in03. No floating gesture marks. |
| 4 jumping | 00-04 | Real upward displacement with bent legs; no sudden overall shrink; returns to baseline. Bottoms203,192,181,193,203. Peak02 top5, versus standing top31-32. |
| 5 failed | 00-07 | Lowered head/gathered arms in02-05 and recovery; readable failure reaction, distinct from idle. |
| 6 waiting | 00-05 | Open palm and expectant expression; distinct asking/approval pose. |
| 7 running / active work | 00-05 | Planted feet, focused chest-level hand activity and blink. No literal running, raised knees or directional travel. |
| 8 review | 00-05 | Head inclination and gathered arms communicate checking/thinking, especially01/02/04; no added paper/UI/prop. |

Across all57: white/lavender hair, horns, wings, dress ornaments and tail preserve the same character. No missing face, eye replacement, changed horn count, detached decorative effect, major clipping, neighboring-cell bleed, obvious seam band, or new torso hole was observed. Dress slit and ornament detail remain recognizable. The shoes in running-right01/05/06 approach the bottom (exclusive bbox bottom207), but a transparent pixel row remains and the shoes are not visibly chopped off. Standing action rows have small1px bottom variations; no unintended baseline pop was observed.

Jump00/04 return within1px of idle's visible bottom203 versus204, which is not a visible landing defect in the native-size comparison.

## All sixteen look meanings

This is labeled visual QA, not a blind verdict. Face landmarks remain readable in all16; no disappeared face, invented eye design, detached pupil, full-body turntable, flipped clothing side or tail reversal was observed.

| Expected direction | Cell | Observed landmark evidence | Verdict |
| --- | --- | --- | --- |
| 000 up | r9/f0 | Raised chin and upward eye line; frontal-up face. | Pass. |
| 022.5 up-right | r9/f1 | Nose/face right of center, gently raised eye line/chin. | Pass; subtle vertical component. |
| 045 up-right | r9/f2 | Rightward nose and eyes, mildly raised chin. | Pass; similar to neighbor. |
| 067.5 up-right | r9/f3 | Stronger right turn while chin/eye line remain slightly up. | Pass; subtle pitch. |
| 090 right | r9/f4 | Nose/profile and eye clearly screen-right. | Pass. |
| 112.5 down-right | r9/f5 | Right-facing head with eye/chin lowering from090. | Pass; subtle down component. |
| 135 down-right | r9/f6 | Clear rightward and forward/downward head pitch. | Pass. |
| 157.5 down-right | r9/f7 | Chin drops toward chest, face remains rightward. | Pass. |
| 180 down | r10/f0 | Frontal lowered head, downcast/closed eyelids and lowered chin. | Pass. |
| 202.5 down-left | r10/f1 | Nose/head left, eyes downcast. | Pass. |
| 225 down-left | r10/f2 | Leftward face and lowered chin/eyes. | Pass; similar to neighbor. |
| 247.5 down-left | r10/f3 | Left-facing head remains slightly down. | Pass; subtle vertical component. |
| 270 left | r10/f4 | Nose/profile and eye clearly screen-left. | Pass. |
| 292.5 up-left | r10/f5 | Left profile with chin/eyes rising from270. | Pass; modest up component. |
| 315 up-left | r10/f6 | Clearer upward pitch of left-facing nose/chin. | Pass. |
| 337.5 up-left | r10/f7 | Raised left-facing nose/chin and upward gaze. | Pass. |

The loop maintains the required principal quadrants with no observed reversal. Several neighboring intermediate angles are very similar and the vertical component near the horizontal cardinals is subtle; those are first-version limitations rather than wrong-axis poses. Fine fingers, lace and ornaments are also small at pet size. The source character's complex long-hair/long-dress design naturally limits the readability of those tiny details.

## Acceptance boundary

This independent visual review finds no remaining hard defect in these exact repaired bytes. Minor muted color traces and subtle intermediate direction differences are recorded above and should not be described as perfect cleanup or uniformly strong angular separation. The report does not certify the structural validator, Pets MCP preflight, Library persistence, upload, activation, or cloud state. Any subsequent byte-changing repair requires fresh exact-byte validation and a new final visual check.
