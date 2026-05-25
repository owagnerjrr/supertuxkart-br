#!/usr/bin/env python3
"""Export Blender-authored Caramelo Dash duo karts to simple B3D files.

Run with Blender:
    blender --background --python art/blender/export_caramelo_dash_b3d.py

This creates static B3D models in the sibling stk-assets folder and points the
four Caramelo Dash kart.xml files at those models.
"""

from __future__ import annotations

import importlib.util
import math
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT.parent / "stk-assets"
SOURCE_SCRIPT = ROOT / "art" / "blender" / "create_caramelo_dash_models.py"

TEAMS = {
    "atho": ("atho", "popo"),
    "popo": ("popo", "atho"),
    "favela": ("favela", "nina"),
    "nina": ("nina", "favela"),
}


def load_source_module():
    spec = importlib.util.spec_from_file_location("caramelo_dash_models", SOURCE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def cstr(value: str) -> bytes:
    return value.encode("utf-8") + b"\0"


def chunk(tag: str, payload: bytes) -> bytes:
    return tag.encode("ascii") + struct.pack("<I", len(payload)) + payload


def material_color(material: bpy.types.Material) -> tuple[float, float, float, float]:
    if material.use_nodes:
        bsdf = next((node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED"), None)
        if bsdf:
            color = bsdf.inputs["Base Color"].default_value
            return (float(color[0]), float(color[1]), float(color[2]), float(color[3]))
    color = material.diffuse_color
    return (float(color[0]), float(color[1]), float(color[2]), float(color[3]))


def blender_to_stk_axis(vector) -> tuple[float, float, float]:
    # The Caramelo Dash modeling script authors vertices directly in STK's
    # coordinate convention: X is lateral, Y is up, and Z is forward.
    return (float(vector.x), float(vector.y), float(vector.z))


def write_scene_b3d(path: Path, objects: list[bpy.types.Object]) -> None:
    depsgraph = bpy.context.evaluated_depsgraph_get()
    vertices: list[tuple[tuple[float, float, float], tuple[float, float, float]]] = []
    triangles_by_material: dict[str, list[tuple[int, int, int]]] = {}
    material_colors: dict[str, tuple[float, float, float, float]] = {}

    for obj in objects:
        if obj.type != "MESH":
            continue
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        matrix = obj.matrix_world.copy()
        normal_matrix = matrix.to_3x3().inverted().transposed()
        material_names = []
        for index, material in enumerate(obj.data.materials):
            name = f"{obj.name}_{index}_{material.name}" if material else f"{obj.name}_{index}_material"
            material_names.append(name)
            if material:
                material_colors[name] = material_color(material)
            else:
                material_colors[name] = (0.8, 0.8, 0.8, 1.0)

        for tri in mesh.loop_triangles:
            mat_index = tri.material_index if tri.material_index < len(material_names) else 0
            mat_name = material_names[mat_index] if material_names else f"{obj.name}_material"
            tri_indices = []
            for vertex_index in tri.vertices:
                vertex = mesh.vertices[vertex_index]
                world_pos = matrix @ vertex.co
                world_normal = (normal_matrix @ vertex.normal).normalized()
                tri_indices.append(len(vertices))
                vertices.append(
                    (
                        blender_to_stk_axis(world_pos),
                        blender_to_stk_axis(world_normal),
                    )
                )
            triangles_by_material.setdefault(mat_name, []).append(tuple(tri_indices))
        evaluated.to_mesh_clear()

    material_names = list(material_colors.keys())
    brus = bytearray(struct.pack("<I", 0))
    for name in material_names:
        r, g, b, a = material_colors[name]
        brus.extend(cstr(name))
        brus.extend(struct.pack("<fffffII", r, g, b, a, 0.0, 1, 0))

    vrts = bytearray(struct.pack("<III", 1, 0, 0))
    for pos, normal in vertices:
        vrts.extend(struct.pack("<ffffff", pos[0], pos[1], pos[2], normal[0], normal[1], normal[2]))

    mesh_payload = bytearray(struct.pack("<i", -1))
    mesh_payload.extend(chunk("VRTS", bytes(vrts)))
    material_id_by_name = {name: idx for idx, name in enumerate(material_names)}
    for name, tris in triangles_by_material.items():
        payload = bytearray(struct.pack("<i", material_id_by_name[name]))
        for tri in tris:
            payload.extend(struct.pack("<III", tri[0], tri[1], tri[2]))
        mesh_payload.extend(chunk("TRIS", bytes(payload)))

    node_payload = bytearray(cstr("caramelo_blender_duo"))
    node_payload.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
    node_payload.extend(struct.pack("<fff", 1.0, 1.0, 1.0))
    node_payload.extend(struct.pack("<ffff", 1.0, 0.0, 0.0, 0.0))
    node_payload.extend(chunk("MESH", bytes(mesh_payload)))

    bb3d = bytearray(struct.pack("<I", 1))
    bb3d.extend(chunk("BRUS", bytes(brus)))
    bb3d.extend(chunk("NODE", bytes(node_payload)))
    path.write_bytes(chunk("BB3D", bytes(bb3d)))


def transform_collection(coll: bpy.types.Collection, loc, scale) -> None:
    for obj in coll.objects:
        obj.location.x = obj.location.x * scale + loc[0]
        obj.location.y = obj.location.y * scale + loc[1]
        obj.location.z = obj.location.z * scale + loc[2]
        obj.scale.x *= scale
        obj.scale.y *= scale
        obj.scale.z *= scale


def add_pet(module, ident: str, coll: bpy.types.Collection) -> None:
    if ident == "atho":
        module.make_cat(coll, "atho", "fur_black", "eye_amber", chubby=False)
    elif ident == "popo":
        module.make_cat(coll, "popo", "fur_white", "eye_green", chubby=True)
    elif ident == "favela":
        module.make_dog(coll, "favela", "fur_caramel", "eye_brown", dark_mask=False)
    elif ident == "nina":
        module.make_dog(coll, "nina", "fur_tan", "eye_brown", dark_mask=True)
    else:
        raise ValueError(ident)


def set_kart_model_xml(kart_xml: Path, model_file: str) -> None:
    tree = ET.parse(kart_xml)
    root = tree.getroot()
    root.set("model-file", model_file)
    for tag in ["animations", "wheels", "headlights", "speed-weighted-objects", "hat"]:
        for child in list(root.findall(tag)):
            root.remove(child)
    tree.write(kart_xml, encoding="utf-8", xml_declaration=True)


def export_team(module, ident: str, front_ident: str, rear_ident: str) -> None:
    module.reset_scene()
    module.mat("fur_black")
    kart_coll = module.collection("duo_kart")
    module.make_duo_kart(kart_coll)

    front = module.collection(f"front_{front_ident}")
    add_pet(module, front_ident, front)
    transform_collection(front, (0.0, 0.42, 0.16), 0.62)

    rear = module.collection(f"rear_{rear_ident}")
    add_pet(module, rear_ident, rear)
    transform_collection(rear, (0.0, 0.44, -0.30), 0.54)

    objects = list(kart_coll.objects) + list(front.objects) + list(rear.objects)
    target_dir = ASSETS / "karts" / ident
    target_dir.mkdir(parents=True, exist_ok=True)
    model_file = f"{ident}_blender_duo.b3d"
    write_scene_b3d(target_dir / model_file, objects)
    set_kart_model_xml(target_dir / "kart.xml", model_file)
    print(f"Exported {ident}: {front_ident} + {rear_ident} -> {target_dir / model_file}")


def main() -> None:
    module = load_source_module()
    for ident, (front_ident, rear_ident) in TEAMS.items():
        export_team(module, ident, front_ident, rear_ident)


if __name__ == "__main__":
    main()
