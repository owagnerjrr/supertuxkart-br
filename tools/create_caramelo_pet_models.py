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
            "pupil": (0.0, 0.0, 0.0, 1.0),
            "collar": (0.78, 0.04, 0.02, 1.0),
            "nose": (0.16, 0.08, 0.06, 1.0),
            "ear": (0.55, 0.20, 0.10, 1.0),
            "whisker": (0.86, 0.86, 0.78, 1.0),
            "scar": (0.95, 0.28, 0.20, 1.0),
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
            "pupil": (0.0, 0.0, 0.0, 1.0),
            "nose": (0.92, 0.45, 0.36, 1.0),
            "ear": (0.92, 0.50, 0.22, 1.0),
            "whisker": (0.90, 0.88, 0.78, 1.0),
            "white": (1.0, 0.97, 0.88, 1.0),
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
            "pupil": (0.0, 0.0, 0.0, 1.0),
            "nose": (0.05, 0.035, 0.025, 1.0),
            "ear": (0.58, 0.24, 0.06, 1.0),
            "muzzle": (0.96, 0.72, 0.42, 1.0),
            "tongue": (0.95, 0.32, 0.42, 1.0),
            "white": (1.0, 0.94, 0.78, 1.0),
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
            "pupil": (0.0, 0.0, 0.0, 1.0),
            "collar": (0.82, 0.10, 0.18, 1.0),
            "nose": (0.04, 0.035, 0.03, 1.0),
            "ear": (0.12, 0.08, 0.055, 1.0),
            "muzzle": (0.78, 0.50, 0.25, 1.0),
            "eyebrow": (0.88, 0.58, 0.26, 1.0),
            "white": (0.96, 0.88, 0.72, 1.0),
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


def add_pupil_pair(mesh, material, center, size):
    cx, cy, cz = center
    add_ellipsoid(mesh, material, (cx - size * 0.75, cy, cz + size * 0.075), (size * 0.13, size * 0.21, size * 0.035), 4, 8)
    add_ellipsoid(mesh, material, (cx + size * 0.75, cy, cz + size * 0.075), (size * 0.13, size * 0.21, size * 0.035), 4, 8)


def add_whiskers(mesh, material, scale, y=0.83, z=0.53, length=0.34):
    for side in (-1, 1):
        x = side * 0.16 * scale
        for offset, slope in [(-0.035, 0.055), (0.0, 0.0), (0.035, -0.055)]:
            add_ellipsoid(
                mesh,
                material,
                (x + side * length * scale * 0.45, (y + offset) * scale, (z + slope) * scale),
                (length * scale, 0.006 * scale, 0.006 * scale),
                3,
                8,
            )


def add_leg_pair(mesh, material, scale, x, z, height=0.30, radius=0.075):
    for side in (-1, 1):
        add_ellipsoid(mesh, material, (side * x * scale, 0.26 * scale, z * scale), (radius * scale, height * scale, radius * 0.95 * scale), 6, 10)
        add_ellipsoid(mesh, material, (side * x * scale, 0.07 * scale, (z + 0.05) * scale), (radius * 1.25 * scale, 0.045 * scale, radius * 1.35 * scale), 4, 10)


def build_pet_mesh(character):
    mesh = Mesh()
    colors = character["colors"]
    kind = character["kind"]
    scale = character["scale"]

    def sc(v):
        x, y, z = v
        return (x * scale, y * scale, z * scale)

    name = character["name"]
    body_radius = (0.34, 0.30, 0.50) if kind == "cat" else (0.40, 0.30, 0.55)
    head_radius = (0.29, 0.27, 0.27)
    if name == "Atho":
        body_radius = (0.30, 0.28, 0.46)
        head_radius = (0.30, 0.27, 0.25)
    elif name == "Popo":
        body_radius = (0.45, 0.36, 0.52)
        head_radius = (0.34, 0.30, 0.28)
    elif name == "Favela":
        body_radius = (0.44, 0.33, 0.56)
        head_radius = (0.34, 0.29, 0.30)
    elif name == "Nina":
        body_radius = (0.48, 0.34, 0.64)
        head_radius = (0.34, 0.29, 0.30)

    add_ellipsoid(mesh, "body", sc((0.0, 0.48, -0.08)), sc(body_radius), 10, 18)
    add_ellipsoid(mesh, "belly", sc((0.0, 0.47, 0.30)), sc((body_radius[0] * 0.62, body_radius[1] * 0.78, 0.055)), 6, 14)
    add_ellipsoid(mesh, "body", sc((0.0, 0.91, 0.25)), sc(head_radius), 10, 18)
    add_leg_pair(mesh, "body", scale, 0.20 if kind == "cat" else 0.23, 0.18, 0.27 if name != "Nina" else 0.33, 0.062 if kind == "cat" else 0.072)
    add_leg_pair(mesh, "body", scale, 0.22 if kind == "cat" else 0.27, -0.25, 0.24 if kind == "cat" else 0.28, 0.062 if kind == "cat" else 0.078)

    if kind == "cat":
        add_cone(mesh, "body", sc((-0.17, 1.10, 0.23)), 0.12 * scale, 0.30 * scale, tilt_x=-0.045 * scale)
        add_cone(mesh, "body", sc((0.17, 1.10, 0.23)), 0.12 * scale, 0.30 * scale, tilt_x=0.045 * scale)
        add_cone(mesh, "ear", sc((-0.17, 1.105, 0.235)), 0.063 * scale, 0.18 * scale, tilt_x=-0.025 * scale)
        add_cone(mesh, "ear", sc((0.17, 1.105, 0.235)), 0.063 * scale, 0.18 * scale, tilt_x=0.025 * scale)
        add_tail(mesh, "body", sc((0.0, 0.58, -0.52)), 0.58 * scale, 0.58 * scale, 0.047 * scale)
        add_whiskers(mesh, "whisker", scale, y=0.84, z=0.53, length=0.28 if name == "Popo" else 0.34)
    else:
        add_ellipsoid(mesh, "ear", sc((-0.29, 0.93, 0.20)), sc((0.085, 0.20, 0.06)), 7, 12)
        add_ellipsoid(mesh, "ear", sc((0.29, 0.93, 0.20)), sc((0.085, 0.20, 0.06)), 7, 12)
        add_tail(mesh, "body", sc((0.0, 0.58, -0.58)), 0.48 * scale, 0.22 * scale, 0.065 * scale)

    add_ellipsoid(mesh, "muzzle" if "muzzle" in colors else "belly", sc((0.0, 0.84, 0.50)), sc((0.15 if kind == "dog" else 0.10, 0.075, 0.09)), 6, 12)
    add_ellipsoid(mesh, "nose", sc((0.0, 0.85, 0.585)), sc((0.075 if kind == "dog" else 0.055, 0.042, 0.035)), 5, 10)
    add_eye_pair(mesh, "eye", sc((0.0, 0.97, 0.47)), 0.23 * scale if kind == "cat" else 0.20 * scale)
    add_pupil_pair(mesh, "pupil", sc((0.0, 0.97, 0.485)), 0.23 * scale if kind == "cat" else 0.20 * scale)

    if "collar" in colors:
        add_ellipsoid(mesh, "collar", sc((0.0, 0.70, 0.30)), sc((0.30, 0.035, 0.23)), 5, 16)

    if name == "Atho":
        add_ellipsoid(mesh, "scar", sc((0.0, 0.90, 0.61)), sc((0.055, 0.012, 0.012)), 3, 8)
        add_ellipsoid(mesh, "collar", sc((0.0, 0.72, 0.35)), sc((0.30, 0.028, 0.055)), 4, 14)
    elif name == "Popo":
        add_ellipsoid(mesh, "white", sc((0.0, 0.91, 0.51)), sc((0.14, 0.18, 0.05)), 6, 12)
        add_ellipsoid(mesh, "patch_a", sc((-0.13, 0.99, 0.49)), sc((0.16, 0.16, 0.045)), 6, 12)
        add_ellipsoid(mesh, "patch_b", sc((0.15, 1.00, 0.47)), sc((0.15, 0.16, 0.045)), 6, 12)
        add_ellipsoid(mesh, "patch_b", sc((-0.18, 0.54, 0.29)), sc((0.18, 0.16, 0.045)), 5, 12)
        add_ellipsoid(mesh, "patch_a", sc((0.20, 0.50, 0.15)), sc((0.15, 0.12, 0.04)), 5, 12)
    elif name == "Favela":
        add_ellipsoid(mesh, "white", sc((0.0, 0.48, 0.36)), sc((0.16, 0.21, 0.05)), 5, 12)
        add_ellipsoid(mesh, "tongue", sc((-0.04, 0.76, 0.60)), sc((0.045, 0.095, 0.028)), 5, 10)
    elif name == "Nina":
        add_ellipsoid(mesh, "muzzle", sc((0.0, 0.82, 0.55)), sc((0.16, 0.08, 0.06)), 6, 12)
        add_ellipsoid(mesh, "eyebrow", sc((-0.13, 1.08, 0.49)), sc((0.055, 0.028, 0.018)), 4, 8)
        add_ellipsoid(mesh, "eyebrow", sc((0.13, 1.08, 0.49)), sc((0.055, 0.028, 0.018)), 4, 8)
        add_ellipsoid(mesh, "white", sc((0.0, 0.46, 0.36)), sc((0.13, 0.18, 0.045)), 5, 12)
        add_ellipsoid(mesh, "patch_a", sc((-0.23, 0.14, 0.22)), sc((0.08, 0.05, 0.09)), 4, 10)
        add_ellipsoid(mesh, "patch_a", sc((0.23, 0.14, 0.22)), sc((0.08, 0.05, 0.09)), 4, 10)

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
