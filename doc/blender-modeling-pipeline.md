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
