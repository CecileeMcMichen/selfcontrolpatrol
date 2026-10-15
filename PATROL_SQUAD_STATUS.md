# Self-Control Patrol v5 — Patrol Squad Character Integration

Status: **COMPLETE.** Every item below was verified by runtime testing in Chromium, except where a line says "static".

The six official Patrol Squad mascots are integrated from the supplied sprite sheets. Gameplay rules, card data, scoring, the save format (`version: 2`) and exports are unchanged.

---

## A. What was added

| File | Purpose |
|---|---|
| `patrol-squad.js` | One shared animation engine for all six characters. It handles states, priority and interruption, pose cross-fades, the talking/blinking head layer, the prop layer, idle scheduling, Reduced Motion, hidden-tab/off-screen/paused handling, and optional voice. |
| `patrol-squad.css` | Board placement, the close-up stage, the motion library (one personality profile per character), prop animations, lineups and Reduced Motion rules. |
| `data/patrol-squad.js` | The runtime character manifest, as a plain script so the game still opens from `file://`. |
| `assets/patrol-squad/manifest.json` | A machine-readable copy of the manifest: assets, source cuts, animations, events and board placement. |
| `assets/patrol-squad/<character>/{poses,expressions,rig,accessories}/` | 294 extracted sprites as true-alpha PNGs, plus 129 `@2x.webp` display copies used at runtime. |
| `tools/patrol-squad-pipeline/` | The extraction, selection, placement and manifest scripts, so the asset set can be reproduced. |

`game.js` changes are limited to the following:

- The placeholder emoji character table was replaced by a thin adapter (`patrolReact`) that reports existing events to the engine.
- Event calls were added inside the existing handlers.
- Three settings were added.
- The four pre-existing bug fixes listed in section F.

`index.html` gains:

- the stylesheet and scripts,
- a board squad layer (beneath the pawns),
- the rebuilt `#patrolCharacter` close-up host,
- Coach Control in the turn spotlight,
- the intro and finale lineups,
- three teacher toggles.

The old placeholder character CSS (four lines of `styles.css`) was retired.

## B. The six characters

| Character | Extracted (poses / expressions / rig parts / accessories) | Board post | Animation personality |
|---|---|---|---|
| Coach Control | 7 / 8 / 36 / 7 | Beside the title, at Headquarters | Energetic: wave, point, cheer, jump, whistle |
| Captain Calm | 8 / 9 / 27 / 2 | Meditating beside the Detention Center | Smooth: slow breathing, eyes open/closed cycle, compass swing |
| Sergeant Pause | 9 / 8 / 39 / 3 | STOP sign raised beside the big THINK sign | Crisp: snap, raise-and-hold pauses, look around |
| Detective Think | 10 / 11 / 13 / 3 | Beside the question-card decks | Inquisitive: tilt, inspect, eureka, magnifier sweep |
| Commander Flex | 8 / 10 / 21 / 5 | Near the Encounter and Social Skills challenges | Springy: bounce, change direction, map unfold |
| Officer Focus | 9 / 8 / 29 / 4 | Beside the progress/task decks with binoculars | Precise: scan, nod, checklist check-off |

Board posts were found by fitting each sprite's actual silhouette onto plain yellow board background. Each post keeps at least 5 px clear of any printed ink and 46 px clear of every one of the 62 playable spaces. No board text, space, pawn or button is covered.

## C. Hybrid presentation

1. **Background Patrol Squad.** All six stand on the board inside the board layer, so they pan and zoom with the camera and sit beneath the pawns.
   - Idle loops are subtle transform-only animations: breathing, a gentle tilt, a springy settle, a scan.
   - Every ~4.6 s one character makes a brief posture shift, using only poses verified not to touch printed art.
   - Captain Calm alternates eyes-open meditation with eyes-closed heart-hands breathing.
2. **Animated close-ups.** The game's existing `#patrolCharacter` reaction element is now a T-shaped close-up that fits the only large open area of the board.
   - A speech bubble spans the decorative title logo. It holds a portrait badge that talks and blinks, an action-prop icon and a short line.
   - A character card stands in the open channel between the title and the THINK sign, with a large full-body figure. The bubble's tail points at the figure.
   - Both pieces keep at least 10 board pixels from the measured edge of every printed space tile. A runtime check confirms that neither piece intersects any of the 62 space tiles.
   - It never touches the card dialog, answer choices, side panel or controls, and it has `pointer-events: none`.
   - While a character is in close-up, its board twin "steps forward" (fades out) and returns afterwards. Board mascots whose post sits under the card (Coach Control and Sergeant Pause) step aside for the same few seconds, so no figure is half-covered.
3. **Coordinated overlays (no duplicate overlays).**
   - Coach Control announces turns inside the existing turn spotlight.
   - Detective Think explains alternatives inside the existing Teaching Ideas panel.
   - Commendations show the matching mascot's portrait.
   - The opening sequence and the Mission Complete finale show the full squad lineup.

## D. Gameplay events → reactions

| Game event (existing handler) | Character | Reaction |
|---|---|---|
| Game opening (`start`) | Coach Control | Greeting close-up: wave → cheer, whistle |
| Player turn begins (`turnSpotlight`) | Coach Control | Points from the turn spotlight; board twin reacts |
| Situation card drawn (stop-and-think) | Sergeant Pause | Alert → raises STOP sign, raise-and-hold |
| Hidden card revealed (question presented) | Detective Think | Thinking → inspect, magnifier sweep |
| Payoff/Consequence card drawn | Detective Think | Compare the choices |
| Power Talk card drawn | Coach Control | Coaching, clipboard check |
| Incorrect first answer | Commander Flex | Change-direction → recovery bounce, map: "New strategy!" |
| Correct first answer | Detective Think | Discovery → idea, eureka |
| Correct after retry | Commander Flex | Recovery celebration |
| Incorrect after retry | Captain Calm | Meditate → eyes-closed breathing, compass: reassuring coaching |
| Physical cue / Anger info / Detention, Trouble, Temper stop | Captain Calm | Breathing / reset |
| Encounter | Sergeant Pause | Stop-and-notice coaching |
| Social skills | Officer Focus | Speaking |
| Charades / exact roll needed | Commander Flex | Flexible encouragement |
| Free turn | Coach Control | Celebration |
| +/− card gain / loss | Officer Focus / Captain Calm | Reward recognition / reset |
| Teacher-scored card (chips earned) | Officer Focus | Approval, checklist |
| Teacher-scored task (persistence) | Officer Focus | "You stayed with it." |
| Timer started / time up | Officer Focus | Focus encouragement |
| Reflection chip | Captain Calm | Encouragement |
| Teaching Ideas opened | Detective Think | Explains alternatives inside the panel |
| Mission complete (`showFinale`) | Entire squad | Finale lineup hops; board squad switches to celebration |

**Priority and interruption.** Answer outcomes have priority 80, card draws 52–60, tasks 50–55 and timers 35, and the finale is 100.

- A higher-priority reaction interrupts the current one.
- A lower-priority reaction waits until the current character finishes its line, then plays. Only one reaction can be queued.
- Repeated triggers within 0.9 s are ignored.
- Undo, Undo Turn, Pause and turn changes clear any visible reaction.
- The engine never changes game state, so it cannot block the turn sequence.

**Language.** Feedback after a wrong answer is always supportive ("Take your time…", "New strategy!"). There are no harsh sounds, no sad faces and no shaming words.

## D2. Best-cut audit (sprite quality pass)

Rule: when a sprite is used, use the clip that looks best when cut. Every runtime sprite was reviewed on the game's dark background, on the yellow board colour and on magenta (which exposes halos and stray pixels). Where a pose existed on more than one sheet, all copies were compared side by side.

**Cleaner v2** (`tools/patrol-squad-pipeline/clean_v2.py`) now runs on every sprite:
- It drops slivers of neighbouring sprites along a cut's edge, plus stray specks.
- It clears faint, disconnected semi-transparent haze.
- It tapers the soft dark glow baked around master-sheet figures to a normal 1–2 px anti-aliased edge, so mascots no longer carry a grey smudge on the yellow board. Opaque art and thin line work (headset cords, lanyards, the carabiner line) are untouched.
- Each sprite keeps its exact canvas size. Board posts and pose heights therefore remain valid.

**Re-picks and removals:**

| Asset | Before | Now | Why |
|---|---|---|---|
| Officer Focus `point-clipboard`, `binoculars-ready` | Slivers of the neighbouring figure on the edge | Same cuts, cleaned | Fragments removed |
| Officer Focus `kneel-binoculars` | `focus_004` | `master_204` | The per-character copy is sliced off at the knees; the master copy is complete |
| Coach Control `whistle` prop | `coach_035` | Bottom of `coach_016` | `coach_035` is a gold lanyard ring, not a whistle (kept as `lanyard-ring`) |
| Detective Think `surprised` face | Used in celebrations | Replaced by `cheerful` | Drawn without her glasses (off-model) |
| Detective Think `idle` pose (`master_130`) | Eligible for board posture shifts | Never shown | Drawn with a monocle instead of her round glasses |

The cuts already chosen elsewhere were confirmed as the best available copy:
- Calm's `calm_a` standing poses over the cropped master copies.
- Pause's `master_082` stop-hand over `pause_000`, which carries a fragment.
- Coach's headset poses over the capped and ponytail master figures.

## E. Animation method (rigging vs. pose swapping)

The hierarchy from the brief was applied per character:

1. **Body-part rigging was tested and rejected for full bodies.** All rig parts were extracted and are documented in the manifest. However, a test assembly of Coach Control showed the parts were drawn at different scales and angles: sleeves were wider than the torso, heads used a different perspective, and the joints left visible gaps. A skeleton built from these parts looked clearly worse than the supplied poses.
2. **Full-body pose swapping** (cross-fades between supplied poses) is used for every character. Sequences never mix the two art styles found in the sheets (see limitations).
3. **Independent part layers** are used where they work well:
   - **Head layer.** The portrait badge has talk cycles, blinks (Captain Calm's eyes-closed, Pause and Flex winks) and expression changes.
   - **Prop layer.** Each prop animates on its own pivot: whistle tweet, compass swing, STOP paddle raise, magnifier sweep, notebook flip, map unfold, binocular scan, checklist check.
4. **Whole-character motion** (transforms only) carries each personality profile.

## F. Pre-existing v5 bugs found during testing and fixed

All four were confirmed in the unmodified v5 package. Each fix is one line, and none changes a game rule.

1. **The opening sequence's START MISSION button did nothing.** `cue()` was undefined, so clicking it raised "cue is not defined" and the intro never closed. The intro sound cues also failed. Fixed with `const cue = name => sound(name)`.
2. **The intro ignored the teacher's Calmer Animations setting.** It checked a non-existent `reduced-motion` class; the game uses `reduce-motion`.
3. **Turns could stall after the last multiple-choice answer.** The action panel was not redrawn, so the **Next player** button never appeared. It now redraws when every question on the card is complete.
4. **Audio was created before any user gesture**, producing browser autoplay warnings. It now waits for the first interaction.

## G. Settings (Teacher → Settings)

- **Show the Patrol Squad on the board.** Default on.
- **Patrol Squad reaction close-ups.** Default on. When off, reactions play on the board characters instead.
- **Patrol Squad voice lines.** Default **off**: a teacher opt-in. It uses the device voice with a per-character pitch and rate, and requires Speech read-aloud to be on. It never interrupts a card being read aloud, it is ducked like other speech, and Quiet preset turns it off. There is no recorded voice acting.

Older saves that lack these keys resume with the defaults.

## H. Verification report

**Runtime-tested in headless Chromium (Playwright).** Results:

- 39/39 gameplay checks (`flow`), including the new check that the close-up never covers a board space tile
- 16/16 layout, mode, voice, offline and performance checks
- the base-game regression run

| Area | Result |
|---|---|
| Every mascot appears; all runtime sprites load | Pass — 6 board actors, 89 runtime files |
| Close-up bubble and card never cover any of the 62 space tiles (runtime geometry check) | Pass |
| Every pose a board mascot can show (23 placements, including posture shifts) sits ≥3 px from printed ink and clear of all spaces — pixel-level, `tools/patrol-squad-pipeline/verify_board.py` | Pass |
| Board mascots under the close-up card step aside and return | Pass |
| Every character line fits the bubble at 1920×1080, 1366×768 and 1024×768 | Pass (the long Teaching Ideas line is shown only in its panel) |
| Board placement avoids all 62 playable spaces | Pass (measured at runtime) |
| Mascot layers never intercept touch | Pass (`pointer-events: none`) |
| Opening → Coach greeting; twin steps forward and returns | Pass |
| Turn → Coach in spotlight; no duplicate close-up | Pass |
| Situation → Sergeant Pause STOP; question → Detective Think | Pass |
| First-try, retry, recovery and incorrect-after-retry each map to the right mascot | Pass |
| Commendation shows the matching mascot; supportive language | Pass |
| Teaching Ideas → Detective Think inside the panel | Pass |
| +/− card → Focus/Calm; Physical cue → Calm breathing pose swap | Pass |
| Teacher award → Focus persistence; Encounter → Pause | Pass |
| Lower-priority reaction queues, then plays | Pass |
| Undo clears reactions; Pause pauses idle animation | Pass |
| Save format v2 unchanged; older save resumes with mascot defaults | Pass |
| Export TSV header unchanged; game log + embedded save | Pass |
| Teacher Reduced Motion and system `prefers-reduced-motion` | Pass: no loops or bounce; message and expression still shown |
| Finale: full squad lineup; board squad switches to celebration | Pass |
| Layouts at 1920×1080 Classroom, 1366×768, 1024×768 and 390×844 | Pass: close-up stays inside the board; no horizontal scroll; text ≥ 11.5 px; on phones reactions play on the board |
| Close-up never overlaps the card dialog or side panel (Classroom) | Pass |
| Voice off by default; opt-in speaks a character line; Speech off silences it | Pass (speech synthesis stubbed) |
| Offline: service worker caches the game and all runtime art; offline reload renders the squad | Pass |
| Performance: 6 compositor animations at idle; about 1.4 MB of mascot art loaded lazily after first paint | Pass |
| 10-player automatic game, 34 turns; unique pawns; tap-target movement; Undo Turn | Pass |
| Console errors or warnings across all runs | None |

**Static inspection only:**

- GitHub Pages and Render static hosting (no build step; all paths are relative).
- Behaviour on physical Smartboard hardware, Safari and Firefox.
- Audible quality of the device voices.

## I. Remaining limitations

- **Two art styles.** The master sheet uses rounder, big-headed figures; the per-character sheets use slimmer ones. Animation sequences stay within one style. Coach Control's board pose (thumbs-up) and some Flex and Focus close-up poses use the slimmer style, so proportions differ slightly between some moments.
- **No eyelid layer on full bodies.** Eyes are part of each full-body pose, so on-body blinking is not possible. Blinks and expressions play on the portrait head. Captain Calm's board idle alternates eyes-open and eyes-closed seated poses.
- **Resolution.** Source poses are only 110–212 px tall. The runtime copies are classic 2× upscales (premultiplied Lanczos plus light sharpening), not AI-upscaled, so close-ups are slightly soft on large Smartboards.
- **Cuts not used:**
  - The Coach row of the master sheet includes poses wearing a blue cap and a pose drawn as a girl with a ponytail. These do not match Coach Control's headset design, so they were excluded.
  - `calm_b` is pixel-identical to `calm_a`.
  - Several cuts were clipped by the sheet edge or carried neighbouring fragments.
  - Detective Think's monocle pose and glasses-free face are extracted but never shown.

  Every rejected cut is listed in `manifest.json` → `rejectedCuts`.
- **Board-specific placement.** Posts are computed for the supplied 1448 × 1086 `board.png`. If the board artwork changes, re-run `tools/patrol-squad-pipeline/fit.py`.
- **Small screens.** The turn-spotlight Coach is hidden below 760 px. Close-ups switch to on-board reactions on boards narrower than 620 px.
