# Brazilian Fauna Racing

Working title for a SuperTuxKart fork inspired by two-rider kart racing.

## Product Direction

- Start with the family pet roster, then expand into Brazilian fauna.
- Include Favela, the cachorro caramelo, as a playable mascot rider.
- Keep SuperTuxKart's arcade handling, item play, split-screen/network base, and existing skidding/drift system.
- Add two-rider karts where one rider drives and the other handles items, with an in-race swap command.

## Initial Playable Roster

The first playable roster is based on the supplied reference photos:

| Ident | Name | Suggested Role |
| --- | --- | --- |
| `atho` | Atho | Black cat with red collar, tight handling |
| `popo` | Popo | Three-color tabby/calico cat, balanced |
| `favela` | Favela | Caramel dog mascot, strong top speed |
| `nina` | Nina | Larger dog with collar, stable/heavier racer |
| `mathias` | Mathias | Darker poodle, technical drift/recovery racer |

ASCII idents are used so asset folders, network packets, and mobile builds stay portable.

## Later Brazilian Fauna Expansion

| Ident | Name | Suggested Role |
| --- | --- | --- |
| `caramelo` | Cachorro Caramelo | Balanced all-rounder |
| `onca-pintada` | Onca-pintada | Heavy speed rider |
| `arara-azul` | Arara-azul | Light acceleration rider |
| `capivara` | Capivara | Stable handling rider |
| `lobo-guara` | Lobo-guara | Drift-focused rider |
| `tamandua-bandeira` | Tamandua-bandeira | Defensive item rider |
| `mico-leao-dourado` | Mico-leao-dourado | High agility rider |
| `boto-cor-de-rosa` | Boto-cor-de-rosa | Trick/item specialist |
| `tucano` | Tucano | Balanced light rider |
| `tatu-bola` | Tatu-bola | Compact defensive rider |

## Implemented Engine Seed

The first code-level seed is intentionally small:

- `KartControl` now has `setSwapRiders()` / `getSwapRiders()` and stores the swap request in the remaining compressed control bit.
- `AbstractKart` now owns a `TeamKartRoster`, which stores front/rear rider ids and exposes `swapTeamRiders()`.
- `TeamKartRoster` lives in `src/karts/team_kart_roster.hpp` and `src/karts/team_kart_roster.cpp`.
- `BrazilianRacingRoster` defines the first five characters and the `50 cc`, `100 cc`, and `150 cc` speed classes.
- `doc/br-menu-double-dash.md` describes the target title, speed-class, pair-selection, and driving-control flow.

This creates the state needed by gameplay, replay/network serialization, UI, and rendering. The next implementation phase should wire an input action to `KartControl::setSwapRiders(true)`, consume that action once per press during race update, and animate rider socket exchange on the kart model.

## Double-Rider Design

Front rider:

- Controls acceleration, steering, braking, and skidding.
- Determines driving voice lines and steering animation.

Rear rider:

- Owns item use, item aim direction, and item voice lines.
- Can have a different item tendency or special item pool later.

Swap behavior:

- Input: one explicit mobile button and one keyboard/controller action.
- Rules: only while racing, not during rescue/explosion/cutscene, and with a short cooldown.
- Effects: front/rear rider ids swap active roles; visual models animate across sockets; item ownership moves to the new rear rider.

## Asset Requirements

SuperTuxKart separates code and full game assets. For development from this repository, the assets need to sit next to the code checkout:

```text
parent/
  supertuxkart-br/
  stk-assets/
```

Each new character should be added as a kart asset folder in the STK asset format, with:

- `kart.xml`
- model mesh and textures
- icon/preview image
- optional voice and animation files
- two rider mount points for front/rear seats

## Mobile Packaging Notes

Android:

- The repository already includes `android/`, `cmake/Toolchain-android.cmake`, and `tools/android_builder.sh`.
- The final Android output is an APK or AAB, depending on the Gradle/build pipeline.
- A real package requires Android SDK/NDK plus the STK assets.

iOS:

- iOS cannot run an APK.
- The iOS output is an `.ipa` generated from an Xcode/iOS toolchain build.
- A signed device build requires macOS, Xcode, and an Apple Developer signing profile.
- The repository already includes `cmake/Toolchain-ios-xcode.cmake` and `data/SuperTuxKart-Info-iOS.plist`.

## Milestones

1. Import assets and verify a stock Android build.
2. Create one playable prototype team: `favela` plus `popo`.
3. Wire swap input to `KartControl::setSwapRiders()`.
4. Consume swap in race update and call `AbstractKart::swapTeamRiders()`.
5. Add rider sockets and swap animation to `KartModel`.
6. Route item/voice behavior through `TeamKartRoster::getActiveRiderIdent()` and `getItemRiderIdent()`.
7. Create full fauna roster and mobile UI polish.
8. Build Android APK/AAB.
9. Build iOS IPA on macOS with signing.

## Licensing

SuperTuxKart is GPL-licensed. A fork based on this code must preserve the applicable GPL obligations. Original fauna assets, names, art, sound, and music should be created or licensed separately.

