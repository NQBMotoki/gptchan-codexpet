# Independent final encoded-atlas visual review

Reviewed: 2026-10-26. Scope: independent visual review of the exact encoded `final/spritesheet.webp`; no artwork changes, upload, activation, or cloud verification.

## Verdict

**Do not mark final visual acceptance complete for these bytes.** Standard animation identity and action semantics remain readable, but there are two blocking visual findings: residual green contamination in the running hair, and a visible upper-body/head registration step at the two look-row boundaries. These are more specific than a generic first-version polish limitation. The direction difference at 292.5 -> 315 is not, by itself, a failure.

Exact reviewed artifact:

- Dimensions: 1536 x 2288, 192 x 208 cells.
- SHA-256: `8d15d2a68e08ad176962b4d6902c4d0cecd6fb69ee446734f9bb4995645dc43c`.
- All 57 standard frames and all 16 look cells were cropped directly from this WEBP, decoded with Pillow, and viewed as ordered native-size cells against `#f0eef6` and `#171923`.
- Existing `contact-final.png` and `direction-labeled.png` were also inspected. No blind answer key, blind verdicts, other reviewers' reports, or generation prompts were read for this review.
- This is an ordered-frame review, not a claim to have observed real-time animation playback. No production art was edited. The only saved visual derivatives are deterministic review crops in `qa/final-independent-evidence/`.

## Blocking findings

### F1: Visible green remnants inside running hair

The final extraction/despill substantially removes the old broad green fringe, but small green islands remain between and along purple hair strands. They are visible at native size on the dark background and become unmistakable in the 2x diagnostic. They are not merely hidden RGB in fully transparent pixels and are not part of the white/lavender approved identity.

Concrete examples, with coordinates relative to the 192 x 208 cell:

- Row 1, running-right frame 00: pale green cluster around x90-94, y82-86, in the rear hair. Pixel (92,82) is RGBA `(157,214,146,255)`; (91,82) is `(159,212,153,255)`.
- Row 1, running-right frame 04: several compact green sections around x73,y111 and x87-88,y87-88. Pixel (73,111) is `(73,148,92,255)` and (88,87) is `(97,150,90,255)`.
- Row 2, running-left frame 04: multiple green patches among the hair curls behind the shoulder and above the tail. Pixel (97,105) is `(73,139,97,255)`; (113,80) is `(130,187,134,222)`.

Evidence: `final-independent-evidence/row-01.png`, `row-02.png`, and `color-detail-2x.png`. The example pixel readings confirm that these visible colored regions survive in the final WEBP; they are not a claim that every green-biased pixel is independently a failure. A diagnostic scan using alpha >=160 and G-max(R,B)>=8 found 36 such pixels in row1/frame00, 48 in row1/frame04, and 58 in row2/frame04. The visual clusters, not the detector alone, determine this finding.

Recommendation: correct the remaining chroma contamination at the appropriate deterministic source/extraction stage, rebuild final bytes, then revalidate and inspect. Do not treat a successful structural validator as proof that these visible remnants are gone.

### F2: Look-family boundary steps are visible, despite a fixed foot baseline

The skirt and feet remain anchored, but the head, neckline, and upper torso make a visible vertical step across the two family boundaries. This looks like the neighboring source families have different upper-body registration/extension, rather than a continuous 22.5-degree gaze step. It should not be dismissed solely because the foot baseline is stable.

- **157.5 -> 180**, row9/frame07 -> row10/frame00: the down-right head/neck at 157.5 sits conspicuously lower; entering 180 lifts the head and collar while retaining a down-looking face. Visible-pixel top changes from y41 to y28; bottom stays y202. Top bounds include horns, so the 13-pixel difference alone is not the verdict: the face, neckline, and shoulder height change together in the native pair.
- **337.5 -> 000**, row10/frame07 -> row9/frame00: the elevated up-left head/neck drops when the face returns toward front-up. Top changes y25 -> y36; bottom remains y202. At native size the shoulder/head assembly settles downward in one step, beyond the small turn of the gaze.
- **292.5 -> 315**, row10/frame05 -> row10/frame06: both tops are y26 and bottoms y202. The larger pixel difference comes mainly from a stronger upward pitch of the face, chin, nose and foreground hair. The torso and skirt remain coherent. I do **not** classify this metric outlier as a hard defect.

Evidence: `final-independent-evidence/seams-native-and-faces.png`, `row-09.png`, `row-10.png`. The first strip includes native full cells and a face detail; its sequence is explicitly labeled and is not a playback claim.

Follow-up landmark check distinguishes this from head pitch alone. `final-independent-evidence/seams-landmark-grid-2x.png` shows the four boundary cells with horizontal guides in original cell coordinates. Approximate hand-read landmark positions have about +/-2px uncertainty:

| Landmark | 157.5 | 180 | 337.5 | 000 |
| --- | ---: | ---: | ---: | ---: |
| Waist/hip flower center | y112 | y106 | y106 | y112 |
| Upper vertex of exposed-thigh/dress opening | y127 | y122 | y122 | y128 |
| Ankle ornament/cuff | y182 | y181 | y180-181 | y182 |
| Final visible bottom (exact alpha bounds) | y202 | y202 | y202 | y202 |

Thus the repeatable 5-7px change reaches the hip and upper thigh while the ankle and ground barely move. This supports a modest longitudinal proportion/scale difference between the two look families, beyond the expected change in face/horn silhouette. It is not a whole-cell translation. I cannot reliably isolate a separate head-size mismatch from the changing yaw/pitch and do not claim one. The 292.5 -> 315 pair retains the lower-body landmarks while changing the head pitch, which is the expected distinction.

Recommendation: inspect and repair the coherent look-family registration/artwork rather than accepting both boundaries as harmless diff outliers. Keep the feet fixed while matching the neck/shoulder/head family through the two boundaries; recheck the complete ordered loop after repair. This review does not prescribe a whole-cell scale change, since face pitch contributes to top bounds.

## Standard-row results (all cells inspected from final bytes)

| Row/state | Cells inspected | Visual result |
| --- | --- | --- |
| 0 idle | 00-05 | Calm blink/micro-variation; same character and stable standing posture. Eyes are readable and are not replaced by a new eye design. |
| 1 running-right | 00-07 | Faces screen-right. Open stride in 00/04 and gathered legs in 01/05 give cadence. Hair and skirt drag left. No wrong-direction frame. F1 remains in hair. |
| 2 running-left | 00-07 | Faces screen-left. 00/04 versus 01/05 provide changing stride; hair/skirt trail right. No temporal or directional reversal observed. F1 remains in hair. |
| 3 waving | 00-03 | Attached hand opens/lifts in 01/02 and returns in 03. No floating wave symbols. |
| 4 jumping | 00-04 | Visible lift and return, preserving apparent body size; no sudden shrink. 00/04 bottoms y203; 01/02/03 bottoms y192/181/193. Peak02 top y5 versus idle top31-32. No pinning to ground. |
| 5 failed | 00-07 | 02-05 lower the head and gather/fold the arms, then recover. The failure reaction is distinct from idle. |
| 6 waiting | 00-05 | Open palm and expectant presentation remain distinct from idle; no new prop or detached symbol. |
| 7 running (active work) | 00-05 | Feet stay planted; hands work near the chest, with focused expression and blink. No literal running, raised knee or directional travel. |
| 8 review | 00-05 | Head tilts/lowers toward gathered arms, especially01/02/04. Readable inspecting/thinking pose without added paper/UI/prop. |

Across these 57 cells, I did not observe a missing face, changed horn count, whole-character identity change, clipped major body part, neighboring-cell bleed, detached decorative effect, obvious seam band, or new hole through the torso. White/lavender hair, horns, wings, dress ornaments and tail remain recognizable. Running-right01/05/06 approach the lower boundary (exclusive bottom207, one transparent pixel remains), but their shoes are not visibly cut off. Standing-row bottoms are approximately203-205, with one-pixel variations; no comparable standard-row registration jump was observed.

The jump is a bent-leg airborne pose rather than character resizing. Its return is within one pixel of the idle bottom (jump203 versus idle204), which is not a visible landing defect in these cells.

Evidence for each standard row: `final-independent-evidence/row-00.png` through `row-08.png`.

## Sixteen look meanings and facial construction

The following is a labeled visual judgment, not a blind-review result. Coordinates are screen/viewer coordinates. Face/eyes remain identifiable in all16, including the side views. The body/skirt/tail do not turn into a rotating full-body turntable. The visible slit/ornaments and tail retain the same side across the loop.

| Direction | Cell | Observed evidence | Meaning verdict |
| --- | --- | --- | --- |
| 000 up | r9/f0 | Chin lifted, eyes above resting line, face pitched upward. | Pass meaning; F2 boundary warning/failure applies separately. |
| 022.5 up-right | r9/f1 | Face and nose shift right, with mildly raised chin/eyes. | Pass, subtle vertical component. |
| 045 up-right | r9/f2 | Nose right of head center; eye/chin line slightly raised. | Pass, close to preceding pose. |
| 067.5 up-right | r9/f3 | Stronger right turn with elevated eye line/chin. | Pass, subtle pitch. |
| 090 right | r9/f4 | Nose/profile and eye clearly screen-right. | Pass. |
| 112.5 down-right | r9/f5 | Right-facing head, gaze/chin drop below the right cardinal. | Pass, subtle down component. |
| 135 down-right | r9/f6 | Rightward face with clear forward/downward pitch. | Pass. |
| 157.5 down-right | r9/f7 | Chin lowers toward chest while face remains rightward. | Pass meaning; F2 outgoing boundary fails continuity. |
| 180 down | r10/f0 | Frontal lowered head, downcast/closed eyelids, chin near chest. | Pass meaning; F2 incoming boundary fails continuity. |
| 202.5 down-left | r10/f1 | Nose and head turn left with downcast eyes. | Pass. |
| 225 down-left | r10/f2 | Leftward face and lowered chin/eyes. | Pass, close to preceding pose. |
| 247.5 down-left | r10/f3 | Head still left and slightly down approaching left cardinal. | Pass, subtle down component. |
| 270 left | r10/f4 | Nose/profile and eye clearly screen-left. | Pass. |
| 292.5 up-left | r10/f5 | Leftward profile; chin/eyes rise from the left cardinal. | Pass, modest up component. |
| 315 up-left | r10/f6 | Face pitches further up-left, raised nose/chin; same eye construction. | Pass; stronger pitch step but no observed hard pop. |
| 337.5 up-left | r10/f7 | Raised left-facing nose/chin and upward gaze. | Pass meaning; F2 outgoing boundary fails continuity. |

I did not observe a wrong principal quadrant, missing cardinal face, eye replacement, pupil detachment, flipped tail, flipped clothing side, or reversed loop order. Similar neighboring intermediate poses and very fine hands/ornaments are mild first-version limitations. They do not excuse F1/F2 above.

## Remaining acceptance boundary

This report does not certify final atlas acceptance, cloud state, upload, or real-time playback. It records visible final-byte defects and specific passes. Any byte-changing repair requires fresh exact-byte validation and another final visual inspection. The two blocking findings should be resolved before claiming the final visual gate has passed.
