# Task 14 - Unified Reduced Motion

Status: COMPLETE

This build unifies the game's reduced-motion behavior across Tasks 1-13.

## Covered systems
- Board atmosphere and destination effects
- Pawn idle, travel, landing, and active-player effects
- Turn spotlight and action-ready effects
- Patrol character reactions
- Patrol Mission card arrival/reveal
- Answer success/recovery/coaching effects
- Flying reward chips and bank feedback
- Patrol Commendations
- Expanded Teaching Ideas
- Headquarters UI transitions
- Animated opening
- Mission Complete finale

## Behavior
- Teacher setting uses the single `reduce-motion` body class.
- Browser/OS `prefers-reduced-motion: reduce` is also respected.
- Essential state information remains visible through text, static highlights, active-player indicators, answer states, score updates, card state, teaching content, and results.
- Reduced Motion changes presentation only; it does not alter scoring, turn rules, card data, response records, save format, or completion logic.
