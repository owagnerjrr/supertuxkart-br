# SuperTuxKart BR Menu and Driving Flow

This document describes the first Brazilian Double Dash-style menu and driving
flow. It is the implementation target for the next UI/gameplay passes.

## Menu Flow

The target first-run flow is:

1. Title screen
   - Show the project identity.
   - Wait for Enter, Start, or the primary confirm button.
2. Speed class
   - Show exactly three choices: `50 cc`, `100 cc`, and `150 cc`.
   - `50 cc` is slower, easier to steer, and friendlier for new players.
   - `100 cc` is the balanced default.
   - `150 cc` is faster, with tighter reaction windows.
3. Character pair selection
   - Player chooses the front rider.
   - Player chooses the rear rider.
   - The same character cannot fill both slots.
   - The selected pair becomes the kart team for the race.
4. Kart/track confirmation
   - Reuse the existing SuperTuxKart flow at first.
   - Later this can become a custom Brazilian cup screen.

## First Character Roster

The initial roster is based on the supplied reference photos:

| Ident | Name | Type | Visual direction | Gameplay direction |
| --- | --- | --- | --- | --- |
| `atho` | Atho | Cat | Black cat, yellow eyes, red collar | Tight handling and quick short acceleration |
| `popo` | Popo | Cat | Three-color tabby/calico coat | Balanced beginner-friendly racer |
| `favela` | Favela | Dog | Caramel dog with white chest | Mascot racer with strong top speed |
| `nina` | Nina | Dog | Larger dog with darker coat and collar | Stable, heavier, good item presence |
| `mathias` | Mathias | Dog | Darker poodle with curly coat | Technical racer, drift and recovery focused |

The code seed for this roster lives in:

```text
src/karts/br_racing_roster.hpp
src/karts/br_racing_roster.cpp
```

## Double Dash-Style Kart System

Each kart should have two riders:

- active/front rider: controls the kart and uses the active item slot
- reserve/rear rider: rides on the kart and can hold a second item

During a race:

- the player can press a swap action to switch front/rear roles
- both riders can carry one item each
- item boxes should fill the active rider first, then the reserve rider if the
  active rider already has an item
- firing uses the active rider item by default

The gameplay-neutral storage for this is seeded in `TeamKartRoster`.

## Driving Feel

The driving target is closer to Speed Drifters than to a steering-wheel mobile
sim:

- acceleration is explicit, not always automatic
- steering should favor left/right arrows or touch buttons
- wheel/tilt steering should not be the default for this project
- drift should be easy to trigger, readable, and useful for corner exits

Initial control target:

| Action | Keyboard | Touch/mobile target |
| --- | --- | --- |
| Accelerate | Up arrow | Right-side accelerate button |
| Brake/reverse | Down arrow | Right-side brake button |
| Steer left | Left arrow | Left arrow button |
| Steer right | Right arrow | Right arrow button |
| Drift | Shift or assigned skid action | Drift button |
| Use item | Space or assigned fire action | Item button |
| Swap riders | New swap action | Swap button near item button |

## Implementation Plan

1. Keep the successful Android build path stable.
2. Add the roster and speed-class data in code.
3. Wire the speed-class choices into the race setup path.
4. Replace or extend the current kart selection screen with a pair-selection
   state.
5. Add HUD indicators for front/rear rider and two item slots.
6. Map swap-rider input to `KartControl::setSwapRiders`.
7. Hook item pickup/use logic into the two rider slots.
8. Build a first Android APK after each visible step.

