#!/usr/bin/env python3
"""Create the first editable Blender source models for Caramelo Dash.

Run with Blender:
    blender --background --python art/blender/create_caramelo_dash_models.py

The generated .blend is the source-of-truth for manual sculpting. It is not
meant to copy Mario Kart Double Dash assets; the kart is an original compact
two-seat prototype for testing the Caramelo Dash double-rider layout.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "art" / "blender" / "generated"
OUT_BLEND = OUT_DIR / "caramelo_dash_models.blend"


PALETTE = {
    "fur_black": (0.008, 0.007, 0.006, 1.0),
    "fur_caramel": (0.95, 0.48, 0.09, 1.0),
    "fur_dark_brown": (0.18, 0.11, 0.065, 1.0),
    "fur_tan": (0.86, 0.53, 0.25, 1.0),
    "fur_white": (1.0, 0.92, 0.78, 1.0),
    "calico_orange": (0.98, 0.46, 0.10, 1.0),
    "eye_amber": (1.0, 0.62, 0.05, 1.0),
    "eye_green": (0.48, 0.90, 0.10, 1.0),
    "eye_brown": (0.55, 0.25, 0.07, 1.0),
    "pupil": (0.0, 0.0, 0.0, 1.0),
    "nose": (0.035, 0.025, 0.020, 1.0),
    "pink": (0.95, 0.32, 0.42, 1.0),
    "collar_red": (0.82, 0.04, 0.03, 1.0),
    "kart_green": (0.04, 0.48, 0.25, 1.0),
    "kart_yellow": (1.0, 0.82, 0.12, 1.0),
    "kart_red": (0.90, 0.05, 0.035, 1.0),
    "rubber": (0.015, 0.014, 0.013, 1.0),
    "metal": (0.72, 0.72, 0.68, 1.0),
}


def reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.68
    return mat


MATS: dict[str, bpy.types.Material] = {}


def mat(name: str) -> bpy.types.Material:
    if not MATS:
        for key, value in PALETTE.items():
            MATS[key] = material(key, value)
    return MATS[name]


def collection(name: str) -> bpy.types.Collection:
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def link_to(obj: bpy.types.Object, coll: bpy.types.Collection) -> bpy.types.Object:
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    coll.objects.link(obj)
    return obj


def shade(obj: bpy.types.Object) -> bpy.types.Object:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    obj.select_set(False)
    return obj


def uv_sphere(
    coll: bpy.types.Collection,
    name: str,
    loc: tuple[float, float, float],
    scale: tuple[float, float, float],
    material_name: str,
    segments: int = 32,
    rings: int = 16,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(material_name))
    link_to(obj, coll)
    return shade(obj)


def cube(
    coll: bpy.types.Collection,
    name: str,
    loc: tuple[float, float, float],
    scale: tuple[float, float, float],
    material_name: str,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(material_name))
    bevel = obj.modifiers.new("soft bevel", "BEVEL")
    bevel.width = 0.08
    bevel.segments = 6
    obj.modifiers.new("smooth shell", "WEIGHTED_NORMAL")
    link_to(obj, coll)
    return obj


def cone(
    coll: bpy.types.Collection,
    name: str,
    loc: tuple[float, float, float],
    radius: float,
    depth: float,
    material_name: str,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat(material_name))
    link_to(obj, coll)
    return shade(obj)


def cylinder(
    coll: bpy.types.Collection,
    name: str,
    loc: tuple[float, float, float],
    radius: float,
    depth: float,
    material_name: str,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat(material_name))
    link_to(obj, coll)
    return shade(obj)


def make_eye_pair(coll: bpy.types.Collection, x: float, y: float, z: float, color: str, size: float) -> None:
    for side in (-1, 1):
        uv_sphere(coll, "eye", (side * x, y, z), (size * 0.70, size, size * 0.22), color)
        uv_sphere(coll, "pupil", (side * x, y - 0.012, z + size * 0.10), (size * 0.28, size * 0.44, size * 0.09), "pupil")
        uv_sphere(coll, "eye_highlight", (side * x - side * size * 0.12, y - 0.030, z + size * 0.24), (size * 0.10, size * 0.11, size * 0.035), "fur_white")


def make_paws(coll: bpy.types.Collection, body_mat: str, length: float, width: float) -> None:
    for x in (-width, width):
        uv_sphere(coll, "front_paw", (x, -0.34, 0.26), (0.13, 0.08, 0.19), body_mat)
        uv_sphere(coll, "rear_paw", (x * 1.12, -0.38, -0.42), (0.15, 0.08, 0.18), body_mat)
        cylinder(coll, "front_leg", (x, -0.15, 0.12), 0.070, length, body_mat)
        cylinder(coll, "rear_leg", (x * 1.12, -0.17, -0.42), 0.082, length * 0.86, body_mat)


def make_tail(coll: bpy.types.Collection, body_mat: str, cat: bool) -> None:
    for i in range(6):
        t = i / 5
        x = 0.0
        y = -0.15 + math.sin(t * math.pi) * (0.45 if cat else 0.18)
        z = -0.72 - t * (0.55 if cat else 0.44)
        radius = (0.065 if cat else 0.085) * (1.0 - t * 0.22)
        uv_sphere(coll, "tail_segment", (x, y, z), (radius, radius, radius * 1.25), body_mat, 20, 10)


def make_cat(coll: bpy.types.Collection, name: str, body: str, eye: str, chubby: bool = False) -> None:
    sx = 1.20 if chubby else 1.0
    sy = 1.10 if chubby else 1.0
    uv_sphere(coll, f"{name}_body", (0, -0.08, -0.12), (0.42 * sx, 0.30 * sy, 0.62), body)
    uv_sphere(coll, f"{name}_head", (0, 0.34, 0.42), (0.38 * sx, 0.33 * sy, 0.32), body)
    make_eye_pair(coll, 0.16 * sx, 0.13, 0.56, eye, 0.105)
    uv_sphere(coll, "muzzle", (0, 0.08, 0.68), (0.16, 0.08, 0.09), "fur_white" if chubby else body)
    uv_sphere(coll, "nose", (0, 0.015, 0.75), (0.060, 0.035, 0.030), "pink" if chubby else "nose")
    cone(coll, "left_ear", (-0.23 * sx, 0.56, 0.37), 0.13, 0.34, body, (0.25, -0.40, 0.0))
    cone(coll, "right_ear", (0.23 * sx, 0.56, 0.37), 0.13, 0.34, body, (0.25, 0.40, 0.0))
    make_paws(coll, body, 0.34, 0.24 * sx)
    make_tail(coll, body, cat=True)
    if name == "atho":
        cylinder(coll, "red_collar", (0, 0.05, 0.34), 0.30, 0.055, "collar_red", (math.pi / 2, 0, 0))
        cube(coll, "nose_scar", (0.0, -0.030, 0.79), (0.070, 0.010, 0.010), "pink")
    else:
        uv_sphere(coll, "white_chest", (0.0, -0.28, 0.22), (0.26, 0.08, 0.32), "fur_white")
        uv_sphere(coll, "black_face_patch", (-0.16, 0.10, 0.58), (0.18, 0.045, 0.18), "fur_black")
        uv_sphere(coll, "orange_face_patch", (0.18, 0.10, 0.57), (0.17, 0.045, 0.18), "calico_orange")
        uv_sphere(coll, "orange_body_patch", (-0.26, -0.18, -0.02), (0.17, 0.055, 0.24), "calico_orange")


def make_dog(coll: bpy.types.Collection, name: str, body: str, eye: str, dark_mask: bool = False) -> None:
    uv_sphere(coll, f"{name}_body", (0, -0.10, -0.12), (0.46, 0.31, 0.72), body)
    uv_sphere(coll, f"{name}_head", (0, 0.34, 0.45), (0.39, 0.33, 0.34), body)
    make_eye_pair(coll, 0.15, 0.12, 0.59, eye, 0.095)
    uv_sphere(coll, "muzzle", (0, 0.02, 0.72), (0.20, 0.11, 0.12), "fur_tan")
    uv_sphere(coll, "nose", (0, -0.055, 0.82), (0.090, 0.055, 0.045), "nose")
    uv_sphere(coll, "tongue", (-0.035, -0.075, 0.74), (0.052, 0.030, 0.11), "pink")
    uv_sphere(coll, "left_ear", (-0.32, 0.32, 0.36), (0.11, 0.07, 0.26), "fur_dark_brown" if dark_mask else "fur_caramel")
    uv_sphere(coll, "right_ear", (0.32, 0.32, 0.36), (0.11, 0.07, 0.26), "fur_dark_brown" if dark_mask else "fur_caramel")
    make_paws(coll, body, 0.40, 0.27)
    make_tail(coll, body, cat=False)
    uv_sphere(coll, "white_chest", (0.0, -0.31, 0.22), (0.18, 0.08, 0.34), "fur_white")
    if dark_mask:
        uv_sphere(coll, "dark_back", (0.0, -0.05, -0.26), (0.48, 0.08, 0.58), "fur_dark_brown")
        uv_sphere(coll, "tan_eyebrow_left", (-0.14, 0.08, 0.67), (0.06, 0.028, 0.025), "fur_tan")
        uv_sphere(coll, "tan_eyebrow_right", (0.14, 0.08, 0.67), (0.06, 0.028, 0.025), "fur_tan")
        cylinder(coll, "red_collar", (0, 0.02, 0.37), 0.32, 0.055, "collar_red", (math.pi / 2, 0, 0))


def make_duo_kart(coll: bpy.types.Collection) -> None:
    cube(coll, "main_rounded_chassis", (0, 0, 0), (0.82, 0.22, 1.05), "kart_green")
    uv_sphere(coll, "yellow_nose", (0, -0.03, 0.75), (0.46, 0.18, 0.35), "kart_yellow")
    cube(coll, "front_seat", (0, 0.25, 0.26), (0.35, 0.10, 0.25), "rubber")
    cube(coll, "rear_seat", (0, 0.27, -0.34), (0.38, 0.10, 0.28), "rubber")
    cylinder(coll, "roll_bar_left", (-0.32, 0.49, -0.08), 0.030, 0.70, "metal", (0.0, 0.0, 0.0))
    cylinder(coll, "roll_bar_right", (0.32, 0.49, -0.08), 0.030, 0.70, "metal", (0.0, 0.0, 0.0))
    cylinder(coll, "front_axle", (0, -0.18, 0.56), 0.035, 1.20, "metal", (0, math.pi / 2, 0))
    cylinder(coll, "rear_axle", (0, -0.18, -0.62), 0.035, 1.28, "metal", (0, math.pi / 2, 0))
    for x in (-0.68, 0.68):
        for z in (0.56, -0.62):
            cylinder(coll, "wheel", (x, -0.18, z), 0.17, 0.16, "rubber", (0, math.pi / 2, 0))
            cylinder(coll, "wheel_hub", (x, -0.18, z), 0.075, 0.175, "kart_red", (0, math.pi / 2, 0))


def add_reference_layout() -> None:
    kart = collection("01_duo_test_kart")
    make_duo_kart(kart)

    atho = collection("02_atho_black_cat")
    make_cat(atho, "atho", "fur_black", "eye_amber", chubby=False)

    popo = collection("03_popo_calico_cat")
    make_cat(popo, "popo", "fur_white", "eye_green", chubby=True)

    favela = collection("04_favela_caramel_dog")
    make_dog(favela, "favela", "fur_caramel", "eye_brown", dark_mask=False)

    nina = collection("05_nina_dark_dog")
    make_dog(nina, "nina", "fur_tan", "eye_brown", dark_mask=True)

    for idx, coll in enumerate([kart, atho, popo, favela, nina]):
        dx = (idx - 2) * 2.2
        for obj in coll.objects:
            obj.location.x += dx


def setup_camera_and_light() -> None:
    bpy.ops.object.light_add(type="AREA", location=(0.0, -5.2, 5.0))
    light = bpy.context.object
    light.name = "large_softbox"
    light.data.energy = 600
    light.data.size = 5.5

    bpy.ops.object.camera_add(location=(0.0, -7.0, 2.8), rotation=(math.radians(68), 0, 0))
    bpy.context.scene.camera = bpy.context.object
    bpy.context.scene.render.resolution_x = 1600
    bpy.context.scene.render.resolution_y = 900


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    reset_scene()
    mat("fur_black")
    add_reference_layout()
    setup_camera_and_light()
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
    print(f"Saved {OUT_BLEND}")


if __name__ == "__main__":
    main()
