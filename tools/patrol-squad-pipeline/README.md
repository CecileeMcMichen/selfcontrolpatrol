# Patrol Squad asset pipeline

These scripts rebuild `assets/patrol-squad/` and `data/patrol-squad.js` from the original sprite sheets. Python 3 with Pillow, NumPy and SciPy is required. **The game itself does not need them.**

Run the steps from a working folder that contains `src/` (the sprite sheets, renamed `master.png`, `coach.png`, `coach_small.png`, `calm_a.png`, `calm_b.png`, `pause.png`, `flex.png`, `focus.png`), `orig/` (the game, for `assets/board.png` and `data/spaces.js`) and `game/` (the output):

1. `segment.py src/<sheet>.png seg/<sheet>` — map every component on a sheet (annotated preview).
2. `cut.py src/<sheet>.png <sheet> cuts` — cut each component with neighbouring pixels masked out.
3. `picks.py` — the best-cut selection: which cut becomes which named pose, expression, rig part or accessory, plus the list of rejected cuts.
4. `build_assets.py cuts game/assets/patrol-squad seg/asset_report.json` — writes the clean, trimmed, true-alpha PNGs and the `@2x.webp` display copies (made with `upscale.py`). Each sprite passes through `clean_v2.py` (neighbour slivers, haze and baked glow removed, canvas size preserved). `rows:<cut>:<y>` picks keep only rows y and below of a cut.
5. `fit.py` — finds board posts by fitting each sprite's silhouette onto plain board background, clear of ink and every space. Writes `seg/board_plan.json`.
6. `hf.py` — the relative pose heights, used so a character keeps a consistent size across poses.
7. `manifest.py` — writes `game/data/patrol-squad.js` and `game/assets/patrol-squad/manifest.json`. It validates every pose, expression and prop reference and rejects any sequence that mixes art styles.
8. `verify_board.py <game folder>` — pixel-level check that every pose a board mascot can show stays clear of printed ink and of every playable space.
