#!/usr/bin/env python3
import argparse
import math
import shutil
import struct
import xml.etree.ElementTree as ET
from pathlib import Path


CHARACTERS = {
    "atho": {
        "name": "Atho",
        "source": "suzanne",
        "type": "light",
        "rgb": "0.02 0.02 0.02",
        "kind": "cat",
        "colors": {
            "body": (0.015, 0.014, 0.013, 1.0),
            "belly": (0.035, 0.032, 0.028, 1.0),
            "eye": (1.0, 0.72, 0.08, 1.0),
            "collar": (0.78, 0.04, 0.02, 1.0),
            "nose": (0.16, 0.08, 0.06, 1.0),
            "ear": (0.55, 0.20, 0.10, 1.0),
        },
        "scale": 0.92,
    },
    "popo": {
        "name": "Popo",
        "source": "suzanne",
        "type": "heavy",
        "rgb": "0.64 0.46 0.28",
        "kind": "cat",
        "colors": {
            "body": (0.92, 0.78, 0.56, 1.0),
            "belly": (1.0, 0.94, 0.82, 1.0),
            "patch_a": (0.05, 0.04, 0.035, 1.0),
            "patch_b": (0.95, 0.45, 0.12, 1.0),
            "eye": (0.60, 0.92, 0.08, 1.0),
            "nose": (0.92, 0.45, 0.36, 1.0),
            "ear": (0.92, 0.50, 0.22, 1.0),
        },
        "scale": 1.08,
    },
    "favela": {
        "name": "Favela",
        "source": "suzanne",
        "type": "medium",
        "rgb": "0.92 0.47 0.05",
        "kind": "dog",
        "colors": {
            "body": (0.90, 0.45, 0.08, 1.0),
            "belly": (0.98, 0.86, 0.66, 1.0),
            "eye": (0.44, 0.22, 0.06, 1.0),
            "nose": (0.05, 0.035, 0.025, 1.0),
            "ear": (0.58, 0.24, 0.06, 1.0),
        },
        "scale": 1.02,
    },
    "nina": {
        "name": "Nina",
        "source": "suzanne",
        "type": "heavy",
        "rgb": "0.58 0.36 0.18",
        "kind": "dog",
        "colors": {
            "body": (0.18, 0.13, 0.09, 1.0),
            "belly": (0.88, 0.62, 0.34, 1.0),
            "patch_a": (0.66, 0.36, 0.14, 1.0),
            "eye": (0.50, 0.24, 0.08, 1.0),
            "collar": (0.82, 0.10, 0.18, 1.0),
            "nose": (0.04, 0.035, 0.03, 1.0),
            "ear": (0.12, 0.08, 0.055, 1.0),
        },
        "scale": 1.16,
    },
}


OBSOLETE = [
    "vira_lata_preto",
    "gato_rajado",
    "capivara",
    "tucano",
    "arara",
    "onca",
    "lobo_guara",
    "tamandua",
    "quati",
    "mico_leao",
    "jacare",
    "preguica",
    "tatu_bola",
    "mathias",
]


class Mesh:
    def __init__(self):
        self.vertices = []
        self.tris_by_material = {}

    def add_vertex(self, position, normal):
        self.vertices.append((position, normal))
        return len(self.vertices) - 1

    def add_tri(self, material, a, b, c):
        self.tris_by_material.setdefault(material, []).append((a, b, c))


def normalize(v):
    x, y, z = v
    length = math.sqrt(x * x + y * y + z * z)
    if length <= 0.00001:
        return (0.0, 1.0, 0.0)
    return (x / length, y / length, z / length)


def add_ellipsoid(mesh, material, center, radius, rings=8, segments=14):
    cx, cy, cz = center
    rx, ry, rz = radius
    grid = []
    for r in range(rings + 1):
        theta = math.pi * r / rings
        row = []
        for s in range(segments):
            phi = 2.0 * math.pi * s / segments
            nx = math.sin(theta) * math.cos(phi)
            ny = math.cos(theta)
            nz = math.sin(theta) * math.sin(phi)
            pos = (cx + rx * nx, cy + ry * ny, cz + rz * nz)
            normal = normalize((nx / max(rx, 0.001), ny / max(ry, 0.001), nz / max(rz, 0.001)))
            row.append(mesh.add_vertex(pos, normal))
        grid.append(row)
    for r in range(rings):
        for s in range(segments):
            a = grid[r][s]
            b = grid[r][(s + 1) % segments]
            c = grid[r + 1][(s + 1) % segments]
            d = grid[r + 1][s]
            mesh.add_tri(material, a, d, c)
            mesh.add_tri(material, a, c, b)


def add_cone(mesh, material, base_center, radius, height, axis="y", segments=14, tilt_x=0.0):
    bx, by, bz = base_center
    tip = (bx + tilt_x, by + height, bz)
    base = []
    for s in range(segments):
        phi = 2.0 * math.pi * s / segments
        pos = (bx + radius * math.cos(phi), by, bz + radius * math.sin(phi))
        base.append(mesh.add_vertex(pos, normalize((pos[0] - bx, height * 0.45, pos[2] - bz))))
    tip_i = mesh.add_vertex(tip, normalize((tilt_x, 1.0, 0.0)))
    center_i = mesh.add_vertex((bx, by, bz), (0.0, -1.0, 0.0))
    for s in range(segments):
        a = base[s]
        b = base[(s + 1) % segments]
        mesh.add_tri(material, a, tip_i, b)
        mesh.add_tri(material, center_i, b, a)


def add_tail(mesh, material, start, length=0.55, curl=0.0, radius=0.045, segments=8):
    sx, sy, sz = start
    points = []
    for i in range(7):
        t = i / 6.0
        x = sx
        y = sy + math.sin(t * math.pi) * curl + t * 0.18
        z = sz - t * length
        points.append((x, y, z))
    rings = []
    for i, p in enumerate(points):
        ring = []
        for s in range(segments):
            phi = 2.0 * math.pi * s / segments
            pos = (p[0] + radius * math.cos(phi), p[1] + radius * math.sin(phi), p[2])
            ring.append(mesh.add_vertex(pos, normalize((math.cos(phi), math.sin(phi), 0.0))))
        rings.append(ring)
    for i in range(len(rings) - 1):
        for s in range(segments):
            a = rings[i][s]
            b = rings[i][(s + 1) % segments]
            c = rings[i + 1][(s + 1) % segments]
            d = rings[i + 1][s]
            mesh.add_tri(material, a, d, c)
            mesh.add_tri(material, a, c, b)


def add_eye_pair(mesh, material, center, size):
    cx, cy, cz = center
    add_ellipsoid(mesh, material, (cx - size * 0.75, cy, cz), (size * 0.34, size * 0.45, size * 0.09), 5, 10)
    add_ellipsoid(mesh, material, (cx + size * 0.75, cy, cz), (size * 0.34, size * 0.45, size * 0.09), 5, 10)


def build_pet_mesh(character):
    mesh = Mesh()
    colors = character["colors"]
    kind = character["kind"]
    scale = character["scale"]

    def sc(v):
        x, y, z = v
        return (x * scale, y * scale, z * scale)

    body_radius = (0.34, 0.25, 0.48) if kind == "cat" else (0.38, 0.27, 0.52)
    if character["name"] == "Popo":
        body_radius = (0.42, 0.32, 0.50)
    if character["name"] == "Nina":
        body_radius = (0.44, 0.30, 0.58)

    add_ellipsoid(mesh, "body", sc((0.0, 0.48, -0.05)), sc(body_radius), 9, 16)
    add_ellipsoid(mesh, "belly", sc((0.0, 0.48, 0.29)), sc((body_radius[0] * 0.55, body_radius[1] * 0.70, 0.045)), 5, 12)
    add_ellipsoid(mesh, "body", sc((0.0, 0.90, 0.24)), sc((0.27, 0.24, 0.25)), 9, 16)

    if kind == "cat":
        add_cone(mesh, "body", sc((-0.16, 1.08, 0.23)), 0.095 * scale, 0.24 * scale, tilt_x=-0.035 * scale)
        add_cone(mesh, "body", sc((0.16, 1.08, 0.23)), 0.095 * scale, 0.24 * scale, tilt_x=0.035 * scale)
        add_cone(mesh, "ear", sc((-0.16, 1.085, 0.235)), 0.052 * scale, 0.15 * scale, tilt_x=-0.02 * scale)
        add_cone(mesh, "ear", sc((0.16, 1.085, 0.235)), 0.052 * scale, 0.15 * scale, tilt_x=0.02 * scale)
        add_tail(mesh, "body", sc((0.0, 0.58, -0.47)), 0.48 * scale, 0.42 * scale, 0.045 * scale)
    else:
        add_ellipsoid(mesh, "ear", sc((-0.27, 0.92, 0.20)), sc((0.08, 0.18, 0.06)), 6, 10)
        add_ellipsoid(mesh, "ear", sc((0.27, 0.92, 0.20)), sc((0.08, 0.18, 0.06)), 6, 10)
        add_tail(mesh, "body", sc((0.0, 0.58, -0.52)), 0.40 * scale, 0.18 * scale, 0.055 * scale)

    add_ellipsoid(mesh, "nose", sc((0.0, 0.84, 0.49)), sc((0.08, 0.055, 0.05)), 5, 10)
    add_eye_pair(mesh, "eye", sc((0.0, 0.94, 0.46)), 0.18 * scale)

    if "collar" in colors:
        add_ellipsoid(mesh, "collar", sc((0.0, 0.70, 0.26)), sc((0.27, 0.035, 0.21)), 5, 14)
    if "patch_a" in colors:
        add_ellipsoid(mesh, "patch_a", sc((-0.11, 0.96, 0.45)), sc((0.12, 0.12, 0.035)), 5, 10)
    if "patch_b" in colors:
        add_ellipsoid(mesh, "patch_b", sc((0.11, 1.00, 0.42)), sc((0.13, 0.12, 0.035)), 5, 10)

    return mesh


def cstr(value):
    return value.encode("utf-8") + b"\0"


def chunk(tag, payload):
    return tag.encode("ascii") + struct.pack("<I", len(payload)) + payload


def write_b3d(path, mesh, colors):
    material_names = list(colors.keys())

    brus = struct.pack("<I", 0)
    for name in material_names:
        r, g, b, a = colors[name]
        brus += cstr(name)
        brus += struct.pack("<fffffII", r, g, b, a, 0.0, 1, 0)

    vrts = struct.pack("<III", 1, 0, 0)
    for pos, normal in mesh.vertices:
        vrts += struct.pack("<ffffff", pos[0], pos[1], pos[2], normal[0], normal[1], normal[2])

    mesh_payload = struct.pack("<i", -1)
    mesh_payload += chunk("VRTS", vrts)
    for material_id, name in enumerate(material_names):
        tris = mesh.tris_by_material.get(name)
        if not tris:
            continue
        payload = struct.pack("<i", material_id)
        for tri in tris:
            payload += struct.pack("<III", tri[0], tri[1], tri[2])
        mesh_payload += chunk("TRIS", payload)

    node_payload = cstr("caramelo_pet")
    node_payload += struct.pack("<fff", 0.0, 0.0, 0.0)
    node_payload += struct.pack("<fff", 1.0, 1.0, 1.0)
    node_payload += struct.pack("<ffff", 1.0, 0.0, 0.0, 0.0)
    node_payload += chunk("MESH", mesh_payload)

    bb3d = struct.pack("<I", 1)
    bb3d += chunk("BRUS", brus)
    bb3d += chunk("NODE", node_payload)
    path.write_bytes(chunk("BB3D", bb3d))


def update_kart_xml(kart_xml, character, model_file):
    tree = ET.parse(kart_xml)
    root = tree.getroot()
    root.set("name", character["name"])
    root.set("type", character["type"])
    root.set("rgb", character["rgb"])
    root.set("groups", "standard")
    root.set("model-file", model_file)
    root.set("icon-file", "icon.png")
    root.set("minimap-icon-file", "icon.png")
    for tag in ["animations", "speed-weighted-objects", "hat"]:
        for child in list(root.findall(tag)):
            root.remove(child)
    tree.write(kart_xml, encoding="utf-8", xml_declaration=True)


def copy_icon(repo_root, target, ident):
    icon = repo_root / "data" / "gui" / "icons" / "characters" / f"{ident}.png"
    if icon.exists():
        shutil.copy2(icon, target / "icon.png")


def prepare_assets(repo_root, assets_path, force):
    karts = assets_path / "karts"
    if not karts.exists():
        raise SystemExit(f"Karts folder not found: {karts}")

    for ident in OBSOLETE:
        target = karts / ident
        if target.exists():
            shutil.rmtree(target)
            print(f"Removed obsolete Caramelo Dash kart {ident}.")

    for ident, character in CHARACTERS.items():
        source = karts / character["source"]
        target = karts / ident
        if not source.exists():
            raise SystemExit(f"Source kart not found: {source}")
        if target.exists():
            if not force:
                print(f"Skipping existing kart {ident}. Use --force to recreate it.")
                continue
            shutil.rmtree(target)
        shutil.copytree(source, target)
        model_file = f"{ident}_pet.b3d"
        write_b3d(target / model_file, build_pet_mesh(character), character["colors"])
        copy_icon(repo_root, target, ident)
        update_kart_xml(target / "kart.xml", character, model_file)
        print(f"Prepared {character['name']} with {model_file}.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--assets-path", default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    assets_path = Path(args.assets_path).resolve() if args.assets_path else (repo_root.parent / "stk-assets").resolve()
    prepare_assets(repo_root, assets_path, args.force)


if __name__ == "__main__":
    main()
