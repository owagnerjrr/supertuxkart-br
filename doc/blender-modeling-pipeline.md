# Caramelo Dash Blender Modeling Pipeline

This folder is the source workflow for replacing the temporary procedural B3D
models with real editable Blender models.

## Goal

Create first-class source models for:

- Favela, caramel dog mascot.
- Nina, larger dark/tan dog with red collar.
- Atho, black cat with red collar.
- Popo, chubby calico cat.
- A single original two-seat test kart for Double Dash-style gameplay.

Do not copy Mario Kart Double Dash assets. Use it only as a reference for the
two-seat kart idea and camera-readable proportions.

## First Pass

Run:

```powershell
blender --background --python art\blender\create_caramelo_dash_models.py
```

Output:

```text
art/blender/generated/caramelo_dash_models.blend
```

Open the `.blend` file and sculpt/refine the collections:

- `01_duo_test_kart`
- `02_atho_black_cat`
- `03_popo_calico_cat`
- `04_favela_caramel_dog`
- `05_nina_dark_dog`

## Mascot Arcade Direction

The next visual direction is not realistic pets. Build one mascot at a time:

- biped body;
- oversized head, eyes, hands, and feet;
- compact torso;
- strong readable color blocks;
- simple accessories;
- selection-screen silhouette first, gameplay detail second.

Start with Favela:

```powershell
blender --background --python art\blender\create_favela_arcade_mascot.py
```

Output:

```text
art/blender/generated/favela_arcade_mascot.blend
art/blender/generated/favela_arcade_mascot_preview.png
```

## Modeling Rules

- Keep silhouettes readable from the kart select camera.
- Use large eyes, clear noses, ears, tails, collars, and body color blocks.
- Popo should be visibly chubby.
- Favela should be caramel, friendly, and mascot-like.
- Nina should look larger, darker, and athletic.
- Atho should be black, compact, and recognizable by red collar and amber eyes.
- Keep the two-seat kart compact, with front and rear rider positions visible.

## Next Export Step

After the `.blend` looks good, export each selected model to a game-friendly
format. The current Android prototype still consumes `.b3d`. For the first
static test export, run:

```powershell
blender --background --python art\blender\export_caramelo_dash_b3d.py
```

This writes:

```text
../stk-assets/karts/atho/atho_blender_duo.b3d
../stk-assets/karts/popo/popo_blender_duo.b3d
../stk-assets/karts/favela/favela_blender_duo.b3d
../stk-assets/karts/nina/nina_blender_duo.b3d
```

and updates each local `kart.xml` in `stk-assets`. These generated game assets
are intentionally not committed to Git.

## STK Coordinate Notes

The Caramelo Dash Blender script authors the model numerically in the same
coordinate convention used by SuperTuxKart:

- `X`: left/right.
- `Y`: up/down.
- `Z`: front/back, with positive `Z` toward the kart front.

Do not apply a second Blender Z-up to STK Y-up conversion in
`export_caramelo_dash_b3d.py`. That makes the exported model vertical on the
wrong axis and places much of the kart below the selection-screen ground plane.

Use this check after exporting:

```powershell
.\tools\inspect_b3d_bounds.ps1 ..\stk-assets\karts\atho\atho_blender_duo.b3d
```

A healthy current export is roughly:

```text
Width  = 1.23
Height = 1.17
Length = 1.83
MinY   = -0.16
MaxY   = 1.01
```

Official STK karts use `*.spm` as the main `model-file` and keep wheels,
headlights, hats, and animated selection frames as separate XML/bone-driven
data. The current Caramelo Dash Blender export is a static `*.b3d`, so the
exporter removes `animations`, `wheels`, `headlights`, `speed-weighted-objects`,
and `hat` nodes from copied official `kart.xml` files to avoid stale bones and
selection animations from the source kart.

## Double-Driver Reference Notes

The `doldecomp/mkdd` project was used as a structural reference only. Do not
copy model data, textures, names, meshes, or proprietary assets from Mario Kart:
Double Dash.

Useful takeaways from the decompiled structure:

- `KartInfo` stores two characters per kart and default partner pairings.
- `KartLoader` builds separate driver models, body model, wheel models, arm
  models, shock models, and shadow model.
- `CharacterSelect3D` has independent selection-screen scale/pose tables for
  characters, kart bodies, arms, dumps, and tires.
- Karts are grouped by light/normal/heavy weight and may have four or six
  wheels.

Caramelo Dash should mirror the readable layout, not the assets: tandem seats,
two visible riders, oversized readable wheels/fenders, clear body color coding,
and character-specific silhouettes.
