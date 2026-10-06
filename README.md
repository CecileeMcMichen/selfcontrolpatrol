# The Self-Control Patrol Game

A shared-screen classroom game built from the supplied board image and workbook. The package is a static site: upload the **contents of this folder** to a GitHub repository. For GitHub Pages, select deployment from the root of the default branch. There is **no build command**; if a host requires one, leave it empty. The publish directory is `/` (repository root). Open `index.html` locally for a quick preview. A served site can cache its files for offline use after the first load.

## Start a game

1. Add 2–10 players, enter a nonempty name or nickname and a unique color for each stop-sign pawn, then choose the Original, 2.0, or combined versions of the Situation, Payoff/Consequence, and +/− decks.
2. Choose an exact-roll finish or a 20, 30, 45, or 60 minute session. Select automatic, drag and drop, or tap-target movement. The setup screen has toggles for multiple-choice cards, Smartboard mode, and card backs.
3. Read the opening briefing **before** the first roll. The workbook directs the teacher to read it only before play; the game holds the first roll until the teacher confirms the briefing.
4. Roll and follow the board. In tap mode, the legal destination glows. In drag mode, roll and place the active pawn, or move that pawn directly as a teacher override. The stop-sign pawns spring along a short arc and land with a boing sound in automatic mode; tap and drag placement gets the same landing animation.
5. Reveal a card, discuss it, then record the outcome. The most recently drawn card remains available under **Teacher → Last card**. On eligible 2.0 cards, each question shuffles its answer order when drawn. A wrong first choice offers another try; a correct choice awards chips, and a second wrong choice highlights the correct answer. After the question is complete, **See more ideas** opens the workbook suggestions. Use the teacher chip controls for any discretionary award.
6. One-minute timers appear on Power Talk, Encounter, and Charades tasks. Start, stop, or restart them. Timed sessions have a separate game clock.

Decks are shuffled **once at the beginning**. A deck reshuffles only when the next card is requested after every card has been drawn. The data has 16 original and 25 2.0 Situation cards; 16 and 25 Payoff cards; 27 and 30 +/− cards; and 12 Power Talk cards. Card wording is imported from the workbook. A separate JSON copy is included for inspection.

## Smartboard and teacher controls

**Classroom Smartboard mode** arranges the supplied 4:3 board on the left and the players, chips, card actions, and turn controls on the right at 1920 × 1080. It enlarges key controls and text, presents a glowing tap target, and keeps the score bank visible above the prompt dialog. A smaller screen stacks the board and controls; long card text can scroll inside its dialog. Use **Full screen** for the best fit. The board and right column are sized for a 1920 × 1080 display; below 1050px wide, they stack and the page scrolls so controls remain usable.

The top-left **Teacher** button opens a panel for manual chip changes, scoring teacher-assessed responses, pause/resume, skip turn, pass a question card, **Undo Turn**, undo the latest action, separate effects and voice switches, read the current or last card aloud, stop speech, Settings, game log, export, Full screen, and a confirmed return to setup. Undo Turn restores the start-of-turn pawn positions, deck cursors and order, active player, score bank, card, pending actions, and turn phase. It remains available immediately after a finishing turn. The adjacent **Instructions** button opens without changing the turn, including while a card is visible. Student-facing score rows have no chip-edit controls.

**Settings** includes separate effects and speech switches, effects volume, a quiet preset, calmer animations, board-camera follow, Smartboard mode, card backs, and multiple-choice display. Distinct roll, card-deal, reveal, chip, task-completion, answer, timer, and finish cues are synthesized locally by the browser. Effects are automatically softened while the device voice reads a card aloud, then return to the selected volume when speech ends or is stopped. Speech uses the device's available voice. The quiet preset sets low effects volume, turns speech off, and reduces motion, and each option remains adjustable. Card flips, chip-count pops, and task-completion glows are brief; pawn travel and these effects respect both the calmer-animation setting and the device's reduced-motion preference. The camera follows an automatically moving pawn only when enabled.

## Progress records and email export

At setup, enter a **Class ID**, class label, school year, optional session notes, and a stable **Student code** for each player. Codes default to `P01`, `P02`, and so on for a single session; replace them with the same teacher-managed codes in later sessions if you want longitudinal comparisons. Use aliases on a shared screen and do not enter unnecessary identifying details.

The game records a response row as soon as a Situation, Payoff, Power Talk, or teacher-assessed task question appears. Multiple-choice rows capture the original (pre-shuffle) choice ID and wording for the first attempt and optional retry, correctness, chip award, and timestamps. The teacher can choose a question in the control panel and add support level and a brief observation. A pending question remains **unfinished** in a mid-session export; a teacher pass is marked **passed**. Game pauses freeze the task and session clocks and persist in the saved state. The saved game includes these records, so the log import preserves progress.

Select **Teacher → Export & email data** at any time. Choose a **Classes**, **Students**, **Sessions**, **Questions**, or **Responses** tab to copy or download its TSV with stable IDs and column headers for a multi-session Google Sheet. The Responses table includes the requested fields plus `Status` and detail columns so incomplete questions remain `unfinished`. The Questions table lists multiple-choice prompts encountered in this session. An optional **Actions TSV** captures the timestamped log. **Open email draft** addresses `cecilee.mcmichen@ocps.net`, with the game title and export date/time in the subject and body and fenced TSV excerpts for the five tables in the body. It opens the device's email app for review and manual sending; a static site cannot send mail or attach files automatically. If the data is long, attach the downloaded full TSV before sending. The export panel also links the reusable `AI_SESSION_ANALYSIS_TEMPLATE.md` for transcript or recording review, optionally combined with the game data.

The **Game log** shows timestamped actions and an embedded save record. Copy the entire text to keep a portable save. On the setup screen, choose **Paste a game log to continue** and paste the complete copied text. The same browser also offers **Resume saved game** from local storage. Names and game progress stay in that browser unless someone copies the log.

## Workbook rules and facilitation

Every player starts with 10 chips. Correct recall on Physical Cue, Anger Information, or Social Skills spaces earns 2. Original Situation responses are awarded 0–5 at the teacher's discretion; original Payoff responses can earn up to 2. Use **Teacher Controls → Score this card/task** to record those results. Power Talk earns 5 unaided or 2 with the card. A +/− card applies its printed value, with an optional reflection chip after a loss. Charades awards 5 to the presenter and 5 to a correct guesser. A detention/trouble/temper stop costs one future turn. An exact roll reaches Patrol Academy; when time expires, the highest chip total wins.

The original Encounter wording describes a teasing exercise. The digital prompt uses an optional, fictional facilitator-led practice scenario for the one-minute activity; students may pass. Review card content for suitability before using it with a group. The workbook includes scanned/typed text with some transcription errors and a later digital-game summary with different point examples; the game follows the first sheet's original rules where these differ.

## Board path

`data/spaces.js` maps centers of the spaces over the **supplied 1448 × 1086 PNG**. Automatic movement follows a practical main route through the left loop and lower road. The upper and central branch spaces are mapped for teacher drag placement. The board does not mark a numbered sequence or explain all branch re-entry choices, so review the coordinates and change `BOARD_SPACES` if your physical route is different. Smartboard tap targeting follows the same main route.

## Files

- `index.html`, `styles.css`, `game.js`: interface and play logic.
- `assets/board.png`: unchanged supplied board artwork; `assets/icon.svg`: app icon.
- `data/cards.js` and `data/cards.json`: workbook cards; `data/spaces.js`: board positions.
- `AI_SESSION_ANALYSIS_TEMPLATE.md`: copy-ready prompt for recorded/transcribed session review.
- `sw.js`: cache for served sites; `export_cards.py`: optional workbook exporter (`python export_cards.py workbook.xlsx`, requires `openpyxl`).

The package includes board art and workbook wording supplied for this project. Check your publication rights before making a repository public.

## Verification and limitations

The package has no build step. The JavaScript syntax and a DOM-driven interaction harness were checked for pawn uniqueness, ten players, pause, reveal, multiple-choice retry and scoring, deck exhaustion, tap/drag/automatic movement, mid-session TSV and email draft, log restore, older v2 save import, and Undo Turn after a finishing turn. The CSS layout was checked against 1920 × 1080 geometry and its stacked smaller-screen rules; a graphical browser was unavailable for pixel-level screenshot review. On a small display, long cards and setup intentionally scroll. A static site opens an email draft but cannot send mail or attach files itself. The existing board-path interpretation and workbook transcription caveats below still apply.

## v4 master-standard update — October 5, 2026

This build retains the v3 board, workbook-derived decks, chip scoring, movement rules, save/log restoration, structured TSV exports, and classroom controls. It adds the project master-standard presentation layer: a remembered/replayable first-time walkthrough, a brief turn-change spotlight and player-name announcement, persistent active-player emphasis already present in the player panel, separate speech volume, and clearer post-resolution **MORE ANSWERS / TEACHING IDEAS** wording. Existing v2/v3 save records remain compatible because the save schema remains version 2; new settings are merged with safe defaults during restore.


## v5 Task 5 checkpoint — Patrol Missions
- Existing card content and scoring/state logic are preserved.
- Situation, Payoff/Consequence, +/- chip, and Power Talk decks now use distinct Patrol Mission identities.
- Card opening uses a Mission Alert banner, deck-specific icon/accent, staged arrival, and reveal animation.
- Card-back mode uses a Mission Alert treatment and Reveal Mission action.
- Classroom Mode scales the mission header for distance viewing.
- Reduced Motion removes travel/flip choreography while preserving mission identity and state changes.


## v5 Task 10 - Self-Control Patrol Sound Identity
- Semantic sound-cue system for turns, missions, movement, landing, answer outcomes, rewards, commendations, teaching, timers, and completion.
- Distinct first-try and recovery success cues; supportive retry/coaching cues.
- Separate Effects, Speech, and Music controls with independent volume sliders.
- Low-volume synthesized Patrol music bed; no external audio dependency required for static/offline hosting.
- Speech ducks effects/music for classroom intelligibility.
- Quiet Preset disables music and speech while retaining low effects.
- Existing save settings remain backward compatible; missing music settings use safe defaults.

---

# v5 COMPLETE CHECKPOINT — PRE-TASK 11

Checkpoint frozen before the full UI/Patrol Headquarters overhaul.

## Production upgrade status

1. Board rebuild architecture — complete; final generated board artwork deferred.
2. Patrol character system — complete; final generated character illustrations deferred.
3. Dimensional pawn/asset system — complete; final generated pawn artwork deferred.
4. Turn event/spotlight system — complete.
5. Patrol Mission card presentation — complete.
6. Enhanced answer feedback — complete.
7. Animated rewards/tokens — complete.
8. Non-scoring Patrol Commendations — complete.
9. Expanded Teaching Ideas experience — complete.
10. Self-Control Patrol sound identity — complete.
11. Full UI upgrade — NOT STARTED in this checkpoint.
12. Animated start sequence — pending.
13. Game finale — pending.
14. Unified Reduced Motion final pass — pending; reduced-motion support already exists across earlier systems.

This checkpoint is intended as the safe rollback baseline before Task 11.


## Task 14 - Unified Reduced Motion
Completed system-wide reduced-motion pass. See `TASK14_STATUS.md`.
