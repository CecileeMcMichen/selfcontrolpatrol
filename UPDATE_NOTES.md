# Self-Control Patrol v5 — Setup and Instructions Update

- Game briefing points are included in Instructions, using the existing in-game read-aloud briefing content.
- Setup retains Class ID with example 2026-501; Class Label and School Year input fields removed.
- Student Code input removed. Internal automatically assigned student IDs and existing export columns are retained for compatibility.
- Patrol mascot names updated to Coach Control, Captain Calm, Sergeant Pause, Detective Think, Commander Flex, and Officer Focus.
- Existing game logic, card data, board, save structure, and export format preserved.
- Patrol Squad artwork integration is not part of this checkpoint; existing mascot reaction graphics remain in place.

## Patrol Squad character integration

- The six Patrol Squad mascots were integrated from the supplied sprite sheets. 294 sprites were extracted with true transparency; the best cut was chosen wherever a sheet contained duplicates.
- **Hybrid presentation:** a background squad stands on clear board areas, animated close-ups play on gameplay events, and the turn spotlight, Teaching Ideas, commendations, intro and finale are coordinated.
- **Settings:** three new teacher switches. Character voice lines are opt-in. Save format v2 is unchanged and older saves are compatible.
- **Fixes:** START MISSION in the intro, the intro's Calmer Animations check, **Next player** after the last multiple-choice answer, and audio before a user gesture.

## Best-cut and close-up pass

- Every runtime sprite was re-audited and cleaned: neighbour slivers, haze and baked edge glow were removed. Officer Focus's kneeling pose now uses the complete copy. Coach's whistle prop is now a real whistle. Detective Think is always shown with her glasses.
- The close-up is now T-shaped: a speech bubble over the title logo, and the character card in the open channel below it. It no longer covers any playable space. Mascots standing under the card step aside while it shows.
