#!/usr/bin/env python3
"""Create Favela as an arcade mascot source model in Blender.

This is intentionally a biped character concept, not a realistic pet model.
It targets a late-90s kart racer selection-screen silhouette: big head, big
eyes, compact body, oversized hands/feet, strong colors, and readable accessory.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "art" / "blender" / "generated"
OUT_BLEND = OUT_DIR / "favela_arcade_mascot.blend"
OUT_PREVIEW = OUT_DIR / "favela_arcade_mascot_preview.png"


COLORS = {
    "caramel_fur": (0.95, 0.49, 0.12, 1.0),
    "dark_ear": (0.45, 0.20, 0.06, 1.0),
    "cream_muzzle": (1.0, 0.78, 0.48, 1.0),
    "white_chest": (1.0, 0.93, 0.76, 1.0),
    "brown_eye": (0.42, 0.18, 0.045, 1.0),
    "black": (0.015, 0.012, 0.010, 1.0),
    "highlight": (1.0, 1.0, 0.92, 1.0),
    "tongue": (0.95, 0.28, 0.38, 1.0),
    "bandana_red": (0.92, 0.05, 0.04, 1.0),
    "glove": (1.0, 0.94, 0.82, 1.0),
    "shoe_green": (0.02, 0.46, 0.22, 1.0),
    "shoe_yellow": (1.0, 0.82, 0.10, 1.0),
    "kart_blue": (0.05, 0.28, 0.85, 1.0),
    "metal": (0.68, 0.70, 0.72, 1.0),
}


def reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.74
    bsdf.inputs["Metallic"].default_value = 0.0
    return mat


MATS: dict[str, bpy.types.Material] = {}


def mat(name: str) -> bpy.types.Material:
    if not MATS:
        for key, value in COLORS.items():
            MATS[key] = material(key, value)
    return MATS[name]


def shade(obj: bpy.types.Object) -> bpy.types.Object:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    obj.select_set(False)
    return obj


def lowpoly(obj: bpy.types.Object) -> bpy.types.Object:
    obj.data.polygons.foreach_set("use_smooth", [False] * len(obj.data.polygons))
    return obj


def sphere(
    name: str,
    loc: tuple[float, float, float],
    scale: tuple[float, float, float],
    material_name: str,
    segments: int = 24,
    rings: int = 12,
    smooth: bool = True,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(material_name))
    return shade(obj) if smooth else lowpoly(obj)


def cube(
    name: str,
    loc: tuple[float, float, float],
    scale: tuple[float, float, float],
    material_name: str,
    bevel: float = 0.04,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(material_name))
    if bevel:
        mod = obj.modifiers.new("arcade bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 4
        obj.modifiers.new("weighted normals", "WEIGHTED_NORMAL")
    return obj


def cylinder(
    name: str,
    loc: tuple[float, float, float],
    radius: float,
    depth: float,
    material_name: str,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
    vertices: int = 18,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat(material_name))
    return shade(obj)


def cone(
    name: str,
    loc: tuple[float, float, float],
    radius: float,
    depth: float,
    material_name: str,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat(material_name))
    return shade(obj)


def add_eye(side: int) -> None:
    x = side * 0.18
    sphere("eye_white", (x, -0.54, 1.70), (0.16, 0.055, 0.20), "highlight", 32, 16)
    sphere("eye_iris", (x, -0.585, 1.68), (0.085, 0.030, 0.115), "brown_eye", 24, 12)
    sphere("eye_pupil", (x, -0.612, 1.67), (0.043, 0.014, 0.060), "black", 16, 8)
    sphere("eye_sparkle", (x - side * 0.035, -0.626, 1.735), (0.025, 0.008, 0.028), "highlight", 12, 6)


def add_hand(name: str, loc: tuple[float, float, float], rot_z: float) -> None:
    palm = sphere(name + "_palm", loc, (0.135, 0.095, 0.135), "glove", 18, 10)
    palm.rotation_euler[2] = rot_z
    for i, dx in enumerate((-0.09, 0.0, 0.09)):
        finger = sphere(f"{name}_finger_{i}", (loc[0] + dx, loc[1] - 0.035, loc[2] + 0.11), (0.040, 0.040, 0.080), "glove", 12, 6)
        finger.rotation_euler[0] = math.radians(18)


def add_shoe(name: str, loc: tuple[float, float, float], side: int) -> None:
    shoe = sphere(name, loc, (0.20, 0.33, 0.105), "shoe_green", 24, 10)
    shoe.rotation_euler[2] = math.radians(8 * side)
    toe = sphere(name + "_toe", (loc[0] + side * 0.015, loc[1] - 0.13, loc[2] + 0.02), (0.15, 0.16, 0.075), "shoe_yellow", 20, 8)
    toe.rotation_euler[2] = math.radians(8 * side)


def build_favela() -> None:
    # Body proportions: small body, oversized head, readable paws.
    sphere("body_caramel", (0.0, 0.0, 0.86), (0.31, 0.23, 0.43), "caramel_fur", 24, 12)
    sphere("white_chest_patch", (0.0, -0.19, 0.90), (0.19, 0.055, 0.30), "white_chest", 18, 10)
    sphere("head_big", (0.0, -0.04, 1.52), (0.47, 0.38, 0.42), "caramel_fur", 32, 16)
    sphere("cheek_left", (-0.18, -0.36, 1.43), (0.19, 0.13, 0.16), "cream_muzzle", 18, 10)
    sphere("cheek_right", (0.18, -0.36, 1.43), (0.19, 0.13, 0.16), "cream_muzzle", 18, 10)
    sphere("muzzle", (0.0, -0.43, 1.39), (0.23, 0.15, 0.16), "cream_muzzle", 24, 12)
    sphere("nose_big", (0.0, -0.57, 1.46), (0.105, 0.065, 0.075), "black", 20, 10)
    sphere("tongue_smile", (0.045, -0.56, 1.30), (0.065, 0.030, 0.095), "tongue", 16, 8)

    add_eye(-1)
    add_eye(1)

    # Floppy ears, strong silhouette.
    left_ear = sphere("left_floppy_ear", (-0.39, -0.05, 1.46), (0.14, 0.075, 0.38), "dark_ear", 20, 10)
    left_ear.rotation_euler = (math.radians(0), math.radians(8), math.radians(-18))
    right_ear = sphere("right_floppy_ear", (0.39, -0.05, 1.46), (0.14, 0.075, 0.38), "dark_ear", 20, 10)
    right_ear.rotation_euler = (math.radians(0), math.radians(-8), math.radians(18))

    # Eyebrows and hair tuft give expression from a distance.
    cube("left_brow", (-0.18, -0.62, 1.88), (0.13, 0.018, 0.028), "dark_ear", 0.015).rotation_euler[2] = math.radians(-10)
    cube("right_brow", (0.18, -0.62, 1.88), (0.13, 0.018, 0.028), "dark_ear", 0.015).rotation_euler[2] = math.radians(10)
    cone("hair_tuft_1", (0.00, -0.08, 2.03), 0.07, 0.22, "dark_ear", (math.radians(-18), 0, 0))
    cone("hair_tuft_2", (-0.08, -0.06, 1.99), 0.055, 0.18, "dark_ear", (math.radians(-25), math.radians(-18), 0))
    cone("hair_tuft_3", (0.08, -0.06, 1.99), 0.055, 0.18, "dark_ear", (math.radians(-25), math.radians(18), 0))

    # Red bandana/collar as Favela's signature accessory.
    cylinder("red_bandana_ring", (0.0, -0.02, 1.13), 0.255, 0.075, "bandana_red", (math.pi / 2, 0, 0), 32)
    cone("bandana_tail_left", (-0.08, 0.18, 1.08), 0.055, 0.22, "bandana_red", (math.radians(100), math.radians(-22), 0))
    cone("bandana_tail_right", (0.08, 0.18, 1.08), 0.055, 0.20, "bandana_red", (math.radians(100), math.radians(22), 0))

    # Arms: one waving, one confident on side.
    cylinder("left_upper_arm", (-0.30, -0.03, 1.06), 0.065, 0.34, "caramel_fur", (math.radians(78), math.radians(-20), math.radians(-35)), 16)
    cylinder("left_forearm", (-0.45, -0.10, 1.27), 0.060, 0.34, "caramel_fur", (math.radians(70), math.radians(-12), math.radians(-18)), 16)
    add_hand("left_wave_hand", (-0.55, -0.18, 1.48), math.radians(-18))

    cylinder("right_upper_arm", (0.30, -0.02, 1.03), 0.065, 0.30, "caramel_fur", (math.radians(92), math.radians(12), math.radians(35)), 16)
    cylinder("right_forearm", (0.43, -0.03, 0.85), 0.060, 0.26, "caramel_fur", (math.radians(70), math.radians(8), math.radians(8)), 16)
    add_hand("right_side_hand", (0.48, -0.13, 0.72), math.radians(10))

    # Legs and oversized arcade shoes.
    cylinder("left_leg", (-0.15, 0.00, 0.48), 0.075, 0.42, "caramel_fur", (0, 0, math.radians(-6)), 16)
    cylinder("right_leg", (0.15, 0.00, 0.48), 0.075, 0.42, "caramel_fur", (0, 0, math.radians(6)), 16)
    add_shoe("left_big_shoe", (-0.18, -0.06, 0.20), -1)
    add_shoe("right_big_shoe", (0.18, -0.06, 0.20), 1)

    # Tail, visible from 3/4 angle.
    for idx, t in enumerate((0.0, 0.25, 0.50, 0.75, 1.0)):
        sphere(
            f"tail_segment_{idx}",
            (0.33 + 0.12 * t, 0.11 + 0.04 * t, 0.78 + math.sin(t * math.pi) * 0.17),
            (0.085 * (1.0 - 0.25 * t), 0.065, 0.090),
            "caramel_fur",
            14,
            8,
        )

    # Tiny kart-themed base helps scale and later integration.
    cube("display_base", (0.0, 0.10, 0.03), (0.55, 0.34, 0.045), "kart_blue", 0.05)
    cylinder("base_front_left_wheel", (-0.39, -0.16, 0.055), 0.075, 0.070, "black", (0, math.pi / 2, 0), 16)
    cylinder("base_front_right_wheel", (0.39, -0.16, 0.055), 0.075, 0.070, "black", (0, math.pi / 2, 0), 16)


def setup_scene() -> None:
    bpy.ops.object.light_add(type="AREA", location=(0.0, -4.5, 4.2))
    key = bpy.context.object
    key.name = "large_softbox_key"
    key.data.energy = 650
    key.data.size = 5.0

    bpy.ops.object.light_add(type="POINT", location=(-2.5, -2.5, 2.0))
    fill = bpy.context.object
    fill.name = "warm_fill"
    fill.data.energy = 70

    bpy.ops.object.camera_add(location=(0.0, -6.2, 1.42), rotation=(math.radians(78), 0, 0))
    cam = bpy.context.object
    bpy.context.scene.camera = cam
    cam.data.lens = 48

    bpy.context.scene.render.engine = "BLENDER_EEVEE"
    if hasattr(bpy.context.scene, "eevee"):
        bpy.context.scene.eevee.taa_render_samples = 64
    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 1500
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.view_settings.look = "Medium High Contrast"
    bpy.context.scene.world.color = (0.78, 0.82, 0.88)


def save_and_render() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
    bpy.context.scene.render.filepath = str(OUT_PREVIEW)
    bpy.ops.render.render(write_still=True)
    print(f"Saved {OUT_BLEND}")
    print(f"Rendered {OUT_PREVIEW}")


def main() -> None:
    reset_scene()
    mat("caramel_fur")
    build_favela()
    setup_scene()
    save_and_render()


if __name__ == "__main__":
    main()
