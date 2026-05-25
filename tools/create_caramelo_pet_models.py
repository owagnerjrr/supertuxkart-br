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

DEFAULT_PARTNERS = {
    "atho": "popo",
    "popo": "atho",
    "favela": "nina",
    "nina": "favela",
}

KART_COLORS = {
    "kart_body": (0.04, 0.48, 0.26, 1.0),
    "kart_body_dark": (0.02, 0.26, 0.16, 1.0),
    "kart_nose": (0.96, 0.84, 0.24, 1.0),
    "kart_trim": (0.94, 0.08, 0.06, 1.0),
    "kart_seat": (0.035, 0.032, 0.030, 1.0),
    "kart_metal": (0.72, 0.72, 0.68, 1.0),
    "kart_wheel": (0.015, 0.014, 0.013, 1.0),
    "kart_hub": (0.82, 0.82, 0.76, 1.0),
    "kart_glass": (0.38, 0.76, 0.95, 0.86),
    "kart_plate": (1.0, 0.97, 0.78, 1.0),
}

KART_STYLES = {
    "atho": {
        "body": (0.03, 0.08, 0.10, 1.0),
        "body_dark": (0.01, 0.018, 0.024, 1.0),
        "nose": (1.0, 0.66, 0.06, 1.0),
        "trim": (0.82, 0.04, 0.03, 1.0),
        "accent": (0.96, 0.92, 0.70, 1.0),
    },
    "popo": {
        "body": (0.98, 0.55, 0.16, 1.0),
        "body_dark": (0.36, 0.22, 0.12, 1.0),
        "nose": (1.0, 0.92, 0.72, 1.0),
        "trim": (0.05, 0.04, 0.035, 1.0),
        "accent": (0.96, 0.38, 0.14, 1.0),
    },
    "favela": {
        "body": (0.04, 0.48, 0.26, 1.0),
        "body_dark": (0.02, 0.28, 0.16, 1.0),
        "nose": (1.0, 0.83, 0.12, 1.0),
        "trim": (0.90, 0.06, 0.04, 1.0),
        "accent": (0.96, 0.68, 0.28, 1.0),
    },
    "nina": {
        "body": (0.10, 0.30, 0.52, 1.0),
        "body_dark": (0.035, 0.10, 0.18, 1.0),
        "nose": (0.78, 0.44, 0.20, 1.0),
        "trim": (0.86, 0.08, 0.16, 1.0),
        "accent": (0.94, 0.72, 0.42, 1.0),
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


def merge_mesh(target, source, offset=(0.0, 0.0, 0.0), scale=1.0, material_prefix=""):
    ox, oy, oz = offset
    first = len(target.vertices)
    for pos, normal in source.vertices:
        target.vertices.append(
            (
                (ox + pos[0] * scale, oy + pos[1] * scale, oz + pos[2] * scale),
                normal,
            )
        )
    for material, tris in source.tris_by_material.items():
        target_material = f"{material_prefix}{material}"
        for a, b, c in tris:
            target.add_tri(target_material, first + a, first + b, first + c)


def prefixed_colors(prefix, colors):
    return {f"{prefix}{name}": value for name, value in colors.items()}


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


def add_cartoon_paw(mesh, material, center, scale, toe_material=None):
    cx, cy, cz = center
    add_ellipsoid(mesh, material, center, (0.095 * scale, 0.045 * scale, 0.12 * scale), 5, 12)
    if toe_material:
        for tx in (-0.045, 0.0, 0.045):
            add_ellipsoid(mesh, toe_material, (cx + tx * scale, cy + 0.025 * scale, cz + 0.075 * scale), (0.018 * scale, 0.012 * scale, 0.012 * scale), 3, 8)


def add_kart_shell(mesh, style):
    # Double-driver silhouette: low toy-like chassis, tandem seats, oversized wheels,
    # and clear fenders. Original geometry, inspired only by the gameplay layout.
    add_ellipsoid(mesh, "kart_body", (0.0, 0.26, -0.06), (0.66, 0.17, 0.92), 8, 20)
    add_ellipsoid(mesh, "kart_body_dark", (0.0, 0.22, -0.08), (0.54, 0.10, 0.74), 5, 18)
    add_ellipsoid(mesh, "kart_nose", (0.0, 0.31, 0.72), (0.42, 0.16, 0.30), 7, 18)
    add_ellipsoid(mesh, "kart_trim", (0.0, 0.43, 0.10), (0.69, 0.035, 0.78), 4, 20)
    add_ellipsoid(mesh, "kart_plate", (0.0, 0.38, 0.98), (0.24, 0.055, 0.035), 3, 10)

    add_ellipsoid(mesh, "kart_seat", (0.0, 0.49, 0.24), (0.31, 0.075, 0.22), 5, 14)
    add_ellipsoid(mesh, "kart_seat", (0.0, 0.52, -0.34), (0.33, 0.078, 0.24), 5, 14)
    add_ellipsoid(mesh, "kart_glass", (0.0, 0.55, 0.55), (0.29, 0.055, 0.045), 4, 12)

    for x in (-0.45, 0.45):
        add_ellipsoid(mesh, "kart_metal", (x, 0.58, 0.16), (0.055, 0.30, 0.045), 5, 10)
        add_ellipsoid(mesh, "kart_metal", (x, 0.62, -0.37), (0.055, 0.32, 0.045), 5, 10)
    add_ellipsoid(mesh, "kart_metal", (0.0, 0.86, 0.16), (0.47, 0.035, 0.045), 4, 14)
    add_ellipsoid(mesh, "kart_metal", (0.0, 0.91, -0.37), (0.49, 0.035, 0.045), 4, 14)

    for x in (-0.58, 0.58):
        for z, radius in ((0.50, 0.21), (-0.58, 0.23)):
            add_ellipsoid(mesh, "kart_wheel", (x, 0.18, z), (0.13, radius, radius), 9, 18)
            add_ellipsoid(mesh, "kart_hub", (x * 1.01, 0.18, z), (0.145, radius * 0.40, radius * 0.40), 6, 12)
            add_ellipsoid(mesh, "kart_trim", (x * 0.88, 0.40, z), (0.22, 0.055, 0.27), 4, 12)

    add_ellipsoid(mesh, "kart_metal", (0.0, 0.28, 0.50), (0.64, 0.035, 0.040), 4, 12)
    add_ellipsoid(mesh, "kart_metal", (0.0, 0.30, -0.58), (0.68, 0.035, 0.040), 4, 12)
    add_ellipsoid(mesh, "kart_trim", (-0.43, 0.42, 0.74), (0.08, 0.055, 0.18), 4, 10)
    add_ellipsoid(mesh, "kart_trim", (0.43, 0.42, 0.74), (0.08, 0.055, 0.18), 4, 10)

    if style:
        for material, key in [
            ("kart_body", "body"),
            ("kart_body_dark", "body_dark"),
            ("kart_nose", "nose"),
            ("kart_trim", "trim"),
            ("kart_plate", "accent"),
        ]:
            KART_COLORS[material] = style[key]


def build_pet_mesh(character):
    mesh = Mesh()
    colors = character["colors"]
    kind = character["kind"]
    scale = character["scale"]

    def sc(v):
        x, y, z = v
        return (x * scale, y * scale, z * scale)

    name = character["name"]
    body_radius = (0.40, 0.25, 0.58) if kind == "cat" else (0.43, 0.27, 0.62)
    head_radius = (0.34, 0.30, 0.29)
    if name == "Atho":
        body_radius = (0.38, 0.24, 0.55)
        head_radius = (0.35, 0.29, 0.27)
    elif name == "Popo":
        body_radius = (0.52, 0.34, 0.58)
        head_radius = (0.38, 0.33, 0.30)
    elif name == "Favela":
        body_radius = (0.48, 0.30, 0.66)
        head_radius = (0.38, 0.32, 0.32)
    elif name == "Nina":
        body_radius = (0.52, 0.31, 0.70)
        head_radius = (0.38, 0.32, 0.32)

    body_y = 0.43 if kind == "cat" else 0.42
    head_y = 0.84 if kind == "cat" else 0.82
    add_ellipsoid(mesh, "body", sc((0.0, body_y, -0.13)), sc(body_radius), 12, 22)
    add_ellipsoid(mesh, "belly", sc((0.0, body_y - 0.02, 0.36)), sc((body_radius[0] * 0.64, body_radius[1] * 0.82, 0.065)), 7, 16)
    add_ellipsoid(mesh, "body", sc((0.0, head_y, 0.34)), sc(head_radius), 12, 22)

    leg_height = 0.20 if kind == "cat" else 0.24
    paw_material = "nose" if kind == "cat" else None
    for side in (-1, 1):
        add_ellipsoid(mesh, "body", sc((side * (0.21 if kind == "cat" else 0.25), 0.20, 0.27)), sc((0.055, leg_height, 0.055)), 6, 10)
        add_cartoon_paw(mesh, "body", sc((side * (0.21 if kind == "cat" else 0.25), 0.04, 0.38)), scale, paw_material)
        add_ellipsoid(mesh, "body", sc((side * (0.26 if kind == "cat" else 0.30), 0.19, -0.36)), sc((0.07, leg_height * 0.85, 0.07)), 6, 10)
        add_cartoon_paw(mesh, "body", sc((side * (0.26 if kind == "cat" else 0.30), 0.04, -0.25)), scale, paw_material)

    if kind == "cat":
        add_cone(mesh, "body", sc((-0.20, 1.04, 0.30)), 0.14 * scale, 0.35 * scale, tilt_x=-0.055 * scale)
        add_cone(mesh, "body", sc((0.20, 1.04, 0.30)), 0.14 * scale, 0.35 * scale, tilt_x=0.055 * scale)
        add_cone(mesh, "ear", sc((-0.20, 1.055, 0.305)), 0.073 * scale, 0.21 * scale, tilt_x=-0.030 * scale)
        add_cone(mesh, "ear", sc((0.20, 1.055, 0.305)), 0.073 * scale, 0.21 * scale, tilt_x=0.030 * scale)
        add_tail(mesh, "body", sc((0.0, 0.52, -0.62)), 0.70 * scale, 0.66 * scale, 0.052 * scale)
        add_whiskers(mesh, "whisker", scale, y=0.77, z=0.62, length=0.30 if name == "Popo" else 0.38)
    else:
        add_ellipsoid(mesh, "ear", sc((-0.32, 0.84, 0.26)), sc((0.10, 0.24, 0.075)), 8, 14)
        add_ellipsoid(mesh, "ear", sc((0.32, 0.84, 0.26)), sc((0.10, 0.24, 0.075)), 8, 14)
        add_tail(mesh, "body", sc((0.0, 0.50, -0.68)), 0.58 * scale, 0.30 * scale, 0.070 * scale)

    add_ellipsoid(mesh, "muzzle" if "muzzle" in colors else "belly", sc((0.0, 0.74, 0.61)), sc((0.18 if kind == "dog" else 0.12, 0.09, 0.105)), 7, 14)
    add_ellipsoid(mesh, "nose", sc((0.0, 0.76, 0.705)), sc((0.088 if kind == "dog" else 0.060, 0.048, 0.040)), 5, 12)
    add_eye_pair(mesh, "eye", sc((0.0, 0.89, 0.56)), 0.28 * scale if kind == "cat" else 0.25 * scale)
    add_pupil_pair(mesh, "pupil", sc((0.0, 0.89, 0.575)), 0.28 * scale if kind == "cat" else 0.25 * scale)

    if "collar" in colors:
        add_ellipsoid(mesh, "collar", sc((0.0, 0.62, 0.37)), sc((0.34, 0.035, 0.25)), 5, 16)

    if name == "Atho":
        add_ellipsoid(mesh, "scar", sc((0.0, 0.80, 0.72)), sc((0.060, 0.012, 0.012)), 3, 8)
        add_ellipsoid(mesh, "collar", sc((0.0, 0.63, 0.42)), sc((0.34, 0.030, 0.060)), 4, 14)
    elif name == "Popo":
        add_ellipsoid(mesh, "white", sc((0.0, 0.82, 0.61)), sc((0.17, 0.20, 0.055)), 6, 12)
        add_ellipsoid(mesh, "patch_a", sc((-0.15, 0.92, 0.58)), sc((0.18, 0.18, 0.050)), 6, 12)
        add_ellipsoid(mesh, "patch_b", sc((0.17, 0.93, 0.56)), sc((0.17, 0.18, 0.050)), 6, 12)
        add_ellipsoid(mesh, "patch_b", sc((-0.20, 0.47, 0.33)), sc((0.20, 0.18, 0.050)), 5, 12)
        add_ellipsoid(mesh, "patch_a", sc((0.23, 0.43, 0.11)), sc((0.17, 0.14, 0.045)), 5, 12)
    elif name == "Favela":
        add_ellipsoid(mesh, "white", sc((0.0, 0.40, 0.40)), sc((0.18, 0.23, 0.055)), 5, 12)
        add_ellipsoid(mesh, "tongue", sc((-0.04, 0.66, 0.72)), sc((0.048, 0.105, 0.030)), 5, 10)
    elif name == "Nina":
        add_ellipsoid(mesh, "muzzle", sc((0.0, 0.72, 0.67)), sc((0.18, 0.09, 0.065)), 6, 12)
        add_ellipsoid(mesh, "eyebrow", sc((-0.14, 1.00, 0.59)), sc((0.065, 0.030, 0.020)), 4, 8)
        add_ellipsoid(mesh, "eyebrow", sc((0.14, 1.00, 0.59)), sc((0.065, 0.030, 0.020)), 4, 8)
        add_ellipsoid(mesh, "white", sc((0.0, 0.38, 0.40)), sc((0.15, 0.20, 0.050)), 5, 12)
        add_ellipsoid(mesh, "patch_a", sc((-0.23, 0.14, 0.22)), sc((0.08, 0.05, 0.09)), 4, 10)
        add_ellipsoid(mesh, "patch_a", sc((0.23, 0.14, 0.22)), sc((0.08, 0.05, 0.09)), 4, 10)

    return mesh


def build_team_kart_mesh(character, partner, style=None):
    mesh = Mesh()
    add_kart_shell(mesh, style)
    merge_mesh(mesh, build_pet_mesh(character), offset=(0.0, 0.42, 0.18), scale=0.44, material_prefix="front_")
    merge_mesh(mesh, build_pet_mesh(partner), offset=(0.0, 0.45, -0.37), scale=0.37, material_prefix="rear_")
    return mesh


def cstr(value):
    return value.encode("utf-8") + b"\0"


def chunk(tag, payload):
    return tag.encode("ascii") + struct.pack("<I", len(payload)) + payload


def write_b3d(path, mesh, colors):
    material_names = list(colors.keys())

    brus = bytearray(struct.pack("<I", 0))
    for name in material_names:
        r, g, b, a = colors[name]
        brus.extend(cstr(name))
        brus.extend(struct.pack("<fffffII", r, g, b, a, 0.0, 1, 0))

    vrts = bytearray(struct.pack("<III", 1, 0, 0))
    for pos, normal in mesh.vertices:
        vrts.extend(struct.pack("<ffffff", pos[0], pos[1], pos[2], normal[0], normal[1], normal[2]))

    mesh_payload = bytearray(struct.pack("<i", -1))
    mesh_payload.extend(chunk("VRTS", bytes(vrts)))
    for material_id, name in enumerate(material_names):
        tris = mesh.tris_by_material.get(name)
        if not tris:
            continue
        payload = bytearray(struct.pack("<i", material_id))
        for tri in tris:
            payload.extend(struct.pack("<III", tri[0], tri[1], tri[2]))
        mesh_payload.extend(chunk("TRIS", bytes(payload)))

    node_payload = bytearray(cstr("caramelo_pet"))
    node_payload.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
    node_payload.extend(struct.pack("<fff", 1.0, 1.0, 1.0))
    node_payload.extend(struct.pack("<ffff", 1.0, 0.0, 0.0, 0.0))
    node_payload.extend(chunk("MESH", bytes(mesh_payload)))

    bb3d = bytearray(struct.pack("<I", 1))
    bb3d.extend(chunk("BRUS", bytes(brus)))
    bb3d.extend(chunk("NODE", bytes(node_payload)))
    path.write_bytes(chunk("BB3D", bytes(bb3d)))


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
        partner = CHARACTERS[DEFAULT_PARTNERS[ident]]
        model_file = f"{ident}_duo_kart.b3d"
        style = KART_STYLES[ident]
        colors = {
            **KART_COLORS,
            **prefixed_colors("front_", character["colors"]),
            **prefixed_colors("rear_", partner["colors"]),
        }
        colors.update({
            "kart_body": style["body"],
            "kart_body_dark": style["body_dark"],
            "kart_nose": style["nose"],
            "kart_trim": style["trim"],
            "kart_plate": style["accent"],
        })
        write_b3d(target / model_file, build_team_kart_mesh(character, partner, style), colors)
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
