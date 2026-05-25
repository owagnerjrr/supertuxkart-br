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
    "caramel_light": (1.0, 0.66, 0.22, 1.0),
    "caramel_shadow": (0.62, 0.28, 0.07, 1.0),
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
    "kart_cyan": (0.00, 0.72, 0.95, 1.0),
    "kart_orange": (1.0, 0.46, 0.08, 1.0),
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


def flattened_sphere(
    name: str,
    loc: tuple[float, float, float],
    scale: tuple[float, float, float],
    material_name: str,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
    segments: int = 24,
    rings: int = 12,
) -> bpy.types.Object:
    obj = sphere(name, loc, scale, material_name, segments, rings)
    obj.rotation_euler = rot
    return obj


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


def torus(
    name: str,
    loc: tuple[float, float, float],
    major_radius: float,
    minor_radius: float,
    material_name: str,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_torus_add(
        major_segments=32,
        minor_segments=8,
        major_radius=major_radius,
        minor_radius=minor_radius,
        location=loc,
        rotation=rot,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat(material_name))
    return shade(obj)


def add_eye(side: int) -> None:
    x = side * 0.18
    sphere("eye_white", (x, -0.55, 1.70), (0.145, 0.050, 0.185), "highlight", 32, 16)
    sphere("eye_iris", (x, -0.590, 1.68), (0.078, 0.028, 0.105), "brown_eye", 24, 12)
    sphere("eye_pupil", (x, -0.616, 1.67), (0.040, 0.013, 0.056), "black", 16, 8)
    sphere("eye_sparkle", (x - side * 0.035, -0.631, 1.735), (0.024, 0.008, 0.027), "highlight", 12, 6)
    flattened_sphere("upper_eyelid", (x, -0.585, 1.82), (0.150, 0.018, 0.035), "caramel_shadow", (math.radians(0), 0, math.radians(4 * side)), 18, 8)


def add_hand(name: str, loc: tuple[float, float, float], rot_z: float) -> None:
    palm = sphere(name + "_palm", loc, (0.150, 0.105, 0.145), "glove", 24, 12)
    palm.rotation_euler[2] = rot_z
    for i, dx in enumerate((-0.09, 0.0, 0.09)):
        finger = sphere(f"{name}_finger_{i}", (loc[0] + dx, loc[1] - 0.045, loc[2] + 0.12), (0.043, 0.043, 0.086), "glove", 16, 8)
        finger.rotation_euler[0] = math.radians(16)
    sphere(name + "_thumb", (loc[0] - 0.105, loc[1] - 0.018, loc[2] + 0.015), (0.052, 0.040, 0.075), "glove", 16, 8)


def add_shoe(name: str, loc: tuple[float, float, float], side: int) -> None:
    shoe = sphere(name, loc, (0.22, 0.35, 0.110), "shoe_green", 28, 12)
    shoe.rotation_euler[2] = math.radians(8 * side)
    toe = sphere(name + "_toe", (loc[0] + side * 0.015, loc[1] - 0.14, loc[2] + 0.025), (0.16, 0.17, 0.078), "shoe_yellow", 22, 10)
    toe.rotation_euler[2] = math.radians(8 * side)
    flattened_sphere(name + "_shine", (loc[0] - side * 0.035, loc[1] - 0.23, loc[2] + 0.095), (0.070, 0.020, 0.018), "highlight", (0, 0, math.radians(8 * side)), 12, 6)


def build_favela() -> None:
    # Body proportions: small body, oversized head, readable paws.
    sphere("body_caramel", (0.0, 0.0, 0.86), (0.32, 0.235, 0.43), "caramel_fur", 30, 14)
    sphere("belly_volume", (0.0, -0.10, 0.76), (0.27, 0.17, 0.32), "caramel_light", 24, 12)
    sphere("white_chest_patch", (0.0, -0.205, 0.91), (0.19, 0.055, 0.30), "white_chest", 24, 12)
    sphere("head_big", (0.0, -0.04, 1.52), (0.49, 0.39, 0.43), "caramel_fur", 40, 18)
    sphere("forehead_light", (0.0, -0.30, 1.68), (0.30, 0.055, 0.25), "caramel_light", 24, 12)
    sphere("cheek_left", (-0.18, -0.365, 1.43), (0.19, 0.13, 0.16), "cream_muzzle", 24, 12)
    sphere("cheek_right", (0.18, -0.365, 1.43), (0.19, 0.13, 0.16), "cream_muzzle", 24, 12)
    sphere("muzzle", (0.0, -0.44, 1.39), (0.24, 0.155, 0.16), "cream_muzzle", 28, 14)
    sphere("nose_big", (0.0, -0.585, 1.47), (0.112, 0.070, 0.078), "black", 24, 12)
    sphere("nose_shine", (-0.035, -0.640, 1.505), (0.030, 0.012, 0.018), "highlight", 12, 6)
    sphere("tongue_smile", (0.045, -0.575, 1.295), (0.065, 0.030, 0.097), "tongue", 18, 8)
    flattened_sphere("left_smile_dimple", (-0.120, -0.590, 1.355), (0.040, 0.010, 0.018), "black", (0, 0, math.radians(-18)), 10, 6)
    flattened_sphere("right_smile_dimple", (0.120, -0.590, 1.355), (0.040, 0.010, 0.018), "black", (0, 0, math.radians(18)), 10, 6)

    add_eye(-1)
    add_eye(1)

    # Floppy ears, strong silhouette.
    left_ear = sphere("left_floppy_ear", (-0.40, -0.05, 1.46), (0.14, 0.075, 0.40), "dark_ear", 24, 12)
    left_ear.rotation_euler = (math.radians(0), math.radians(8), math.radians(-18))
    sphere("left_inner_ear", (-0.405, -0.085, 1.43), (0.085, 0.028, 0.30), "caramel_shadow", 18, 8).rotation_euler = (0, math.radians(8), math.radians(-18))
    right_ear = sphere("right_floppy_ear", (0.40, -0.05, 1.46), (0.14, 0.075, 0.40), "dark_ear", 24, 12)
    right_ear.rotation_euler = (math.radians(0), math.radians(-8), math.radians(18))
    sphere("right_inner_ear", (0.405, -0.085, 1.43), (0.085, 0.028, 0.30), "caramel_shadow", 18, 8).rotation_euler = (0, math.radians(-8), math.radians(18))

    # Eyebrows and hair tuft give expression from a distance.
    cube("left_brow", (-0.18, -0.625, 1.875), (0.13, 0.018, 0.026), "dark_ear", 0.015).rotation_euler[2] = math.radians(-10)
    cube("right_brow", (0.18, -0.625, 1.875), (0.13, 0.018, 0.026), "dark_ear", 0.015).rotation_euler[2] = math.radians(10)
    cone("hair_tuft_1", (0.00, -0.08, 2.03), 0.07, 0.22, "dark_ear", (math.radians(-18), 0, 0))
    cone("hair_tuft_2", (-0.08, -0.06, 1.99), 0.055, 0.18, "dark_ear", (math.radians(-25), math.radians(-18), 0))
    cone("hair_tuft_3", (0.08, -0.06, 1.99), 0.055, 0.18, "dark_ear", (math.radians(-25), math.radians(18), 0))

    # Red bandana/collar as Favela's signature accessory.
    torus("red_bandana_ring", (0.0, -0.02, 1.13), 0.245, 0.030, "bandana_red", (math.pi / 2, 0, 0))
    sphere("bandana_knot", (0.0, 0.18, 1.11), (0.060, 0.050, 0.050), "bandana_red", 14, 8)
    cone("bandana_tail_left", (-0.08, 0.18, 1.08), 0.055, 0.22, "bandana_red", (math.radians(100), math.radians(-22), 0))
    cone("bandana_tail_right", (0.08, 0.18, 1.08), 0.055, 0.20, "bandana_red", (math.radians(100), math.radians(22), 0))

    # Arms: one waving, one confident on side.
    sphere("left_shoulder", (-0.29, -0.01, 1.08), (0.080, 0.075, 0.080), "caramel_shadow", 14, 8)
    cylinder("left_upper_arm", (-0.31, -0.03, 1.08), 0.065, 0.34, "caramel_fur", (math.radians(78), math.radians(-20), math.radians(-35)), 18)
    cylinder("left_forearm", (-0.45, -0.10, 1.29), 0.060, 0.34, "caramel_fur", (math.radians(70), math.radians(-12), math.radians(-18)), 18)
    add_hand("left_wave_hand", (-0.55, -0.18, 1.48), math.radians(-18))

    sphere("right_shoulder", (0.29, -0.01, 1.05), (0.080, 0.075, 0.080), "caramel_shadow", 14, 8)
    cylinder("right_upper_arm", (0.30, -0.02, 1.03), 0.065, 0.30, "caramel_fur", (math.radians(92), math.radians(12), math.radians(35)), 18)
    cylinder("right_forearm", (0.43, -0.03, 0.85), 0.060, 0.26, "caramel_fur", (math.radians(70), math.radians(8), math.radians(8)), 18)
    add_hand("right_side_hand", (0.48, -0.13, 0.72), math.radians(10))

    # Legs and oversized arcade shoes.
    cylinder("left_leg", (-0.15, 0.00, 0.48), 0.077, 0.42, "caramel_fur", (0, 0, math.radians(-6)), 18)
    cylinder("right_leg", (0.15, 0.00, 0.48), 0.077, 0.42, "caramel_fur", (0, 0, math.radians(6)), 18)
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
    cube("display_base", (0.0, 0.10, 0.03), (0.60, 0.36, 0.045), "kart_blue", 0.05)
    cube("display_base_stripe", (0.0, -0.09, 0.083), (0.36, 0.030, 0.012), "kart_cyan", 0.012)
    cube("display_base_front", (0.0, -0.245, 0.055), (0.28, 0.035, 0.018), "kart_orange", 0.018)
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
