#!/usr/bin/env python3
"""Generate SVG/PNG figures for lecture notes.

Uses consistent, clean rendering for nodes, edges, arrows, and labels.
Graphs follow the same style as the only-tree-graph images:
  - nodes drawn on top of edges/arrows
  - arrowheads centered on the middle of each edge
  - edge labels as small white badges with dark text
  - matrices drawn with clear cell grids and proper subscript/superscript
"""
import os
import math
import cairosvg

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)


# Colors and sizes
NODE_FILL = "#1e3a5f"
NODE_INNER = "#ffffff"
EDGE = "#1e3a5f"
TWIG = "#2b6cb0"
LINK = "#e53e3e"
CUTSET = "#dd6b20"
BG = "#fafbfc"
TEXT = "#2d3748"
LIGHT = "#718096"

NODE_RADIUS = 6
ARROW_SIZE = 11
LABEL_OFFSET = 16
LABEL_BOX_W = 20
LABEL_BOX_H = 16
LABEL_FONT_SIZE = 12
BULGE_DIST = 48
EDGE_WIDTH = 3


def save_svg(name, svg_content):
    svg_path = os.path.join(FIG_DIR, f"{name}.svg")
    png_path = os.path.join(FIG_DIR, f"{name}.png")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to=png_path, scale=2.0)
    print(f"Saved {svg_path} and {png_path}")


def svg_start(w, h, title=""):
    aria = f' aria-label="{title}"' if title else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"{aria}>
  <rect width="{w}" height="{h}" fill="{BG}"/>
'''


def svg_end():
    return "</svg>\n"


def normalize(vx, vy):
    d = math.hypot(vx, vy)
    return vx / d, vy / d


def add(p, v, s):
    return p[0] + v[0] * s, p[1] + v[1] * s


def subscript_text(base, sub, x, y, size=14, color=TEXT, font_weight="bold"):
    """SVG text with subscript using tspan."""
    sub_size = int(size * 0.7)
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" font-family="sans-serif" '
        f'font-size="{size}" fill="{color}" font-weight="{font_weight}">'
        f'{base}<tspan dy="{int(size*0.35)}" font-size="{sub_size}">{sub}</tspan></text>'
    )


def plain_text(text, x, y, size=14, color=TEXT, anchor="middle", font_weight="normal"):
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" font-family="sans-serif" '
        f'font-size="{size}" fill="{color}" font-weight="{font_weight}">{text}</text>'
    )


def node(cx, cy, label="", lx=0, ly=-18):
    """Draw a node with label above/below."""
    g = (
        f'<circle cx="{cx}" cy="{cy}" r="{NODE_RADIUS}" fill="{NODE_FILL}" stroke="none"/>\n'
        f'<circle cx="{cx}" cy="{cy}" r="{NODE_RADIUS * 0.4}" fill="{NODE_INNER}" opacity="0.22"/>\n'
    )
    if label:
        g += plain_text(label, cx + lx, cy + ly, size=14, color=TEXT, font_weight="bold")
    return g


def curve_points(x1, y1, x2, y2, side):
    """Return control points for a cubic Bezier edge from (x1,y1) to (x2,y2).
    side=1 bulges one way, side=-1 the other, side=0 means straight."""
    if side == 0:
        return (x1, y1), (x1, y1), (x2, y2), (x2, y2)
    p0 = (x1, y1)
    p3 = (x2, y2)
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return p0, p0, p3, p3
    ox = (dy / length) * BULGE_DIST
    oy = (-dx / length) * BULGE_DIST
    if side == -1:
        ox, oy = -ox, -oy
    p1 = (x1 + (mx - x1) / 2 + ox * 0.55, y1 + (my - y1) / 2 + oy * 0.55)
    p2 = (x2 - (x2 - mx) / 2 + ox * 0.55, y2 - (y2 - my) / 2 + oy * 0.55)
    return p0, p1, p2, p3


def trim_curve(p0, p1, p2, p3, r):
    """Trim cubic Bezier endpoints to distance r from source/target nodes."""
    if p1 == p0 and p2 == p3:
        t0x, t0y = normalize(p3[0] - p0[0], p3[1] - p0[1])
        t1x, t1y = t0x, t0y
    else:
        t0x, t0y = normalize(p1[0] - p0[0], p1[1] - p0[1])
        t1x, t1y = normalize(p3[0] - p2[0], p3[1] - p2[1])
    p0_new = add(p0, (t0x, t0y), r)
    p3_new = add(p3, (-t1x, -t1y), r)
    side = None
    if p0_new != p3_new and (p1 != p0 or p2 != p3):
        mx = (p0[0] + p3[0]) / 2
        my = (p0[1] + p3[1]) / 2
        qx = 0.125 * (p0[0] + 3 * p1[0] + 3 * p2[0] + p3[0])
        qy = 0.125 * (p0[1] + 3 * p1[1] + 3 * p2[1] + p3[1])
        dx = p3[0] - p0[0]
        dy = p3[1] - p0[1]
        cross = (qx - mx) * dy - (qy - my) * dx
        if cross > 0:
            side = 1
        elif cross < 0:
            side = -1
    return p0_new, p1, p2, p3_new, side


def recompute_curve(p0, p3, side):
    """Recompute control points for the trimmed endpoints with same bulge."""
    if side == 0 or side is None:
        return p0, p0, p3, p3
    return curve_points(p0[0], p0[1], p3[0], p3[1], side)


def edge_path(p0, p1, p2, p3):
    if p1 == p0 and p2 == p3:
        return f'M {p0[0]:.2f} {p0[1]:.2f} L {p3[0]:.2f} {p3[1]:.2f}'
    return f'M {p0[0]:.2f} {p0[1]:.2f} C {p1[0]:.2f} {p1[1]:.2f}, {p2[0]:.2f} {p2[1]:.2f}, {p3[0]:.2f} {p3[1]:.2f}'


def bezier_midpoint_and_tangent(p0, p1, p2, p3):
    """Return point and tangent at t=0.5 of a cubic Bezier curve."""
    mx = 0.125 * (p0[0] + 3 * p1[0] + 3 * p2[0] + p3[0])
    my = 0.125 * (p0[1] + 3 * p1[1] + 3 * p2[1] + p3[1])
    tx = 0.75 * (-p0[0] - p1[0] + p2[0] + p3[0])
    ty = 0.75 * (-p0[1] - p1[1] + p2[1] + p3[1])
    d = math.hypot(tx, ty)
    if d == 0:
        tx, ty = p3[0] - p0[0], p3[1] - p0[1]
        d = math.hypot(tx, ty)
        if d == 0:
            return (mx, my), (1, 0)
    return (mx, my), (tx / d, ty / d)


def centered_arrow(x, y, ux, uy, size, fill, stroke):
    """Arrowhead polygon centered at (x,y) pointing along (ux,uy)."""
    px, py = -uy, ux
    base_x = x - ux * (size / 2)
    base_y = y - uy * (size / 2)
    tip_x = x + ux * (size / 2)
    tip_y = y + uy * (size / 2)
    b1x = base_x + px * (size / 2)
    b1y = base_y + py * (size / 2)
    b2x = base_x - px * (size / 2)
    b2y = base_y - py * (size / 2)
    return (
        f'<polygon points="{tip_x:.2f},{tip_y:.2f} {b2x:.2f},{b2y:.2f} {b1x:.2f},{b1y:.2f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.2" stroke-linejoin="round"/>'
    )


def edge_label_badge(x, y, text, color=EDGE, bg="#ffffff"):
    """Small white badge with branch number."""
    w = LABEL_BOX_W
    h = LABEL_BOX_H
    rx = 3
    sx = x - w / 2
    sy = y - h / 2
    return (
        f'<rect x="{sx:.2f}" y="{sy:.2f}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{bg}" stroke="{color}" stroke-width="0.8"/>'
        f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" dominant-baseline="middle" '
        f'font-family="sans-serif" font-size="{LABEL_FONT_SIZE}" fill="{color}" font-weight="bold">{text}</text>'
    )


def draw_edge_with_arrow_and_label(x1, y1, x2, y2, side=0, color=EDGE, width=EDGE_WIDTH,
                                    directed=False, label="", label_badge=True):
    """Draw an edge, then a midpoint arrow, then an offset label."""
    p0, p1, p2, p3 = curve_points(x1, y1, x2, y2, side)
    p0, p1, p2, p3, side_found = trim_curve(p0, p1, p2, p3, NODE_RADIUS)
    p0, p1, p2, p3 = recompute_curve(p0, p3, side_found)

    path = f'<path d="{edge_path(p0, p1, p2, p3)}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" fill="none"/>'

    (mx, my), (ux, uy) = bezier_midpoint_and_tangent(p0, p1, p2, p3)
    extra = ""
    if directed:
        extra += centered_arrow(mx, my, ux, uy, ARROW_SIZE, "#ffffff", color)

    if label:
        # label offset to the left of the directed edge
        lx = mx - uy * LABEL_OFFSET
        ly = my + ux * LABEL_OFFSET
        if label_badge:
            extra += edge_label_badge(lx, ly, label, color=color)
        else:
            extra += plain_text(label, lx, ly, size=LABEL_FONT_SIZE, color=TEXT, font_weight="bold")

    return path + extra


# ============================================================
# Lecture 1 figures
# ============================================================


def fig_01_01_graph_abc():
    svg = svg_start(500, 220, "A simple graph with three nodes")
    svg += draw_edge_with_arrow_and_label(120, 110, 250, 60, label="1")
    svg += draw_edge_with_arrow_and_label(250, 60, 250, 160, label="2")
    svg += draw_edge_with_arrow_and_label(120, 110, 250, 160, label="3")
    svg += node(120, 110, label="A")
    svg += node(250, 60, label="B")
    svg += node(250, 160, label="C", ly=18)
    svg += f'<text x="380" y="90" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}" font-weight="bold">Graph G = (V, E)</text>'
    svg += f'<text x="380" y="115" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">V = {{A, B, C}}</text>'
    svg += f'<text x="380" y="135" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">E = {{1, 2, 3}}</text>'
    svg += svg_end()
    save_svg("fig-01-01-graph-abc", svg)


def fig_01_02_directed_graph():
    svg = svg_start(500, 220, "A directed graph")
    svg += draw_edge_with_arrow_and_label(120, 110, 250, 60, directed=True, label="1")
    svg += draw_edge_with_arrow_and_label(250, 60, 250, 160, directed=True, label="2")
    svg += draw_edge_with_arrow_and_label(120, 110, 250, 160, directed=True, label="3")
    svg += node(120, 110, label="A")
    svg += node(250, 60, label="B")
    svg += node(250, 160, label="C", ly=18)
    svg += f'<text x="380" y="90" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}" font-weight="bold">Directed Graph</text>'
    svg += f'<text x="380" y="115" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">Arrow = orientation</text>'
    svg += svg_end()
    save_svg("fig-01-02-directed-graph", svg)


def fig_01_03_connected_disconnected():
    svg = svg_start(640, 220, "Connected vs disconnected graph")
    # Connected graph
    svg += f'<text x="140" y="35" text-anchor="middle" font-family="sans-serif" font-size="14" fill="{TEXT}" font-weight="bold">Connected</text>'
    svg += draw_edge_with_arrow_and_label(80, 110, 140, 70)
    svg += draw_edge_with_arrow_and_label(140, 70, 200, 110)
    svg += draw_edge_with_arrow_and_label(80, 110, 200, 110)
    svg += node(80, 110, label="A")
    svg += node(140, 70, label="B")
    svg += node(200, 110, label="C")
    # Disconnected graph
    svg += f'<text x="480" y="35" text-anchor="middle" font-family="sans-serif" font-size="14" fill="{TEXT}" font-weight="bold">Disconnected</text>'
    svg += draw_edge_with_arrow_and_label(420, 110, 480, 70)
    svg += draw_edge_with_arrow_and_label(480, 70, 560, 110)
    svg += node(420, 110, label="A")
    svg += node(480, 70, label="B")
    svg += node(560, 110, label="C")
    svg += node(560, 170, label="D", ly=18)
    svg += svg_end()
    save_svg("fig-01-03-connected-disconnected", svg)


def fig_01_04_cycle():
    svg = svg_start(500, 220, "A cycle graph")
    svg += draw_edge_with_arrow_and_label(120, 110, 250, 60, label="1")
    svg += draw_edge_with_arrow_and_label(250, 60, 250, 160, label="2")
    svg += draw_edge_with_arrow_and_label(250, 160, 120, 110, label="3")
    svg += node(120, 110, label="A")
    svg += node(250, 60, label="B")
    svg += node(250, 160, label="C", ly=18)
    svg += f'<text x="360" y="100" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}" font-weight="bold">A – B – C – A</text>'
    svg += f'<text x="360" y="125" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">Forms a cycle</text>'
    svg += svg_end()
    save_svg("fig-01-04-cycle", svg)


def fig_01_05_tree():
    svg = svg_start(500, 220, "A tree graph")
    svg += draw_edge_with_arrow_and_label(120, 110, 250, 60, label="1")
    svg += draw_edge_with_arrow_and_label(250, 60, 250, 160, label="2")
    svg += node(120, 110, label="A")
    svg += node(250, 60, label="B")
    svg += node(250, 160, label="C", ly=18)
    svg += f'<text x="360" y="90" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}" font-weight="bold">Tree</text>'
    svg += f'<text x="360" y="115" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">3 nodes, 2 edges</text>'
    svg += f'<text x="360" y="135" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">No cycles</text>'
    svg += svg_end()
    save_svg("fig-01-05-tree", svg)


def fig_01_06_spanning_trees_triangle():
    svg = svg_start(640, 220, "Three spanning trees of a triangle")
    positions = [
        (120, 120, 220, 70, 220, 170, "{1,2}", "A", "B", "C"),
        (320, 120, 420, 70, 420, 170, "{2,3}", "A", "B", "C"),
        (520, 120, 620, 70, 620, 170, "{1,3}", "A", "B", "C"),
    ]
    for i, (x1, y1, x2, y2, x3, y3, s, la, lb, lc) in enumerate(positions):
        if i == 0:
            edges = [(x1, y1, x2, y2, "1"), (x2, y2, x3, y3, "2")]
        elif i == 1:
            edges = [(x2, y2, x3, y3, "2"), (x3, y3, x1, y1, "3")]
        else:
            edges = [(x1, y1, x2, y2, "1"), (x3, y3, x1, y1, "3")]
        for x1e, y1e, x2e, y2e, label in edges:
            svg += draw_edge_with_arrow_and_label(x1e, y1e, x2e, y2e, label=label)
        svg += node(x1, y1, label=la)
        svg += node(x2, y2, label=lb)
        svg += node(x3, y3, label=lc, ly=18)
        svg += plain_text(s, (x1 + x2) / 2, 195, size=12, color=TEXT)
    svg += svg_end()
    save_svg("fig-01-06-spanning-trees-triangle", svg)


# ============================================================
# Lecture 2 figures
# ============================================================


def draw_table(x0, y0, data, cell_w=40, cell_h=30, font_size=14, header=True):
    """Draw a simple table with equal cells."""
    rows = len(data)
    cols = len(data[0])
    s = ""
    for i in range(rows):
        for j in range(cols):
            fill = BG
            if header and i == 0:
                fill = "#edf2f7"
            elif j == 0 and i > 0:
                fill = "#edf2f7"
            x = x0 + j * cell_w
            y = y0 + i * cell_h
            s += f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="#cbd5e0" stroke-width="0.5"/>'
            s += plain_text(data[i][j], x + cell_w / 2, y + cell_h / 2 + 5, size=font_size, color=TEXT)
    return s


def fig_02_01_incidence_matrix():
    svg = svg_start(640, 260, "Incidence matrix example")
    # Triangle graph A->B, B->C, C->A
    svg += draw_edge_with_arrow_and_label(120, 120, 240, 60, directed=True, label="1")
    svg += draw_edge_with_arrow_and_label(240, 60, 240, 180, directed=True, label="2")
    svg += draw_edge_with_arrow_and_label(240, 180, 120, 120, directed=True, label="3")
    svg += node(120, 120, label="A")
    svg += node(240, 60, label="B")
    svg += node(240, 180, label="C", ly=18)

    svg += subscript_text("A", "a", 375, 55, size=16, color=TEXT)

    table = [
        ["", "1", "2", "3"],
        ["A", "+1", "0", "-1"],
        ["B", "-1", "+1", "0"],
        ["C", "0", "-1", "+1"],
    ]
    svg += draw_table(360, 80, table, cell_w=45, cell_h=30, font_size=14)
    svg += f'<text x="360" y="210" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">Remove one row (e.g. C) to get</text>'
    svg += f'<text x="360" y="228" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">reduced incidence matrix</text>'
    svg += svg_end()
    save_svg("fig-02-01-incidence-matrix", svg)


def fig_02_02_laplacian_matrix():
    svg = svg_start(640, 260, "Laplacian matrix example")
    svg += draw_edge_with_arrow_and_label(120, 120, 240, 60)
    svg += draw_edge_with_arrow_and_label(240, 60, 240, 180)
    svg += draw_edge_with_arrow_and_label(240, 180, 120, 120)
    svg += node(120, 120, label="A")
    svg += node(240, 60, label="B")
    svg += node(240, 180, label="C", ly=18)

    svg += f'<text x="360" y="55" text-anchor="start" font-family="sans-serif" font-size="18" fill="{TEXT}" font-weight="bold">L</text>'
    table = [
        ["", "A", "B", "C"],
        ["A", "2", "-1", "-1"],
        ["B", "-1", "2", "-1"],
        ["C", "-1", "-1", "2"],
    ]
    svg += draw_table(360, 80, table, cell_w=45, cell_h=30, font_size=14)
    svg += f'<text x="360" y="210" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">L = A</text>'
    svg += subscript_text("A", "a", 425, 210, size=12, color=LIGHT, font_weight="normal")
    svg += f'<text x="440" y="210" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">A</text>'
    svg += subscript_text("A", "a", 454, 210, size=12, color=LIGHT, font_weight="normal")
    svg += f'<text x="451" y="206" text-anchor="start" font-family="sans-serif" font-size="10" fill="{LIGHT}">ᵀ</text>'
    svg += f'<text x="360" y="228" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">Diagonal = degree, off-diagonal = -#edges</text>'
    svg += svg_end()
    save_svg("fig-02-02-laplacian-matrix", svg)


def fig_02_03_matrix_tree_theorem():
    svg = svg_start(640, 240, "Matrix-Tree theorem")
    svg += draw_edge_with_arrow_and_label(120, 110, 240, 60)
    svg += draw_edge_with_arrow_and_label(240, 60, 240, 160)
    svg += draw_edge_with_arrow_and_label(240, 160, 120, 110)
    svg += node(120, 110, label="A")
    svg += node(240, 60, label="B")
    svg += node(240, 160, label="C", ly=18)

    svg += f'<text x="320" y="75" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}">1. Build L</text>'
    svg += f'<text x="320" y="100" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}">2. Delete row/col k</text>'
    svg += f'<text x="320" y="125" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}">3. det(L</text>'
    svg += f'<text x="392" y="125" text-anchor="start" font-family="sans-serif" font-size="10" fill="{TEXT}">(k)</text>'
    svg += f'<text x="410" y="125" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}">) = τ(G)</text>'
    svg += f'<text x="320" y="165" text-anchor="start" font-family="sans-serif" font-size="18" fill="{NODE_FILL}" font-weight="bold">τ(G) = 3</text>'
    svg += svg_end()
    save_svg("fig-02-03-matrix-tree-theorem", svg)


def fig_02_04_6_node_special_laplacian():
    svg = svg_start(820, 420, "6-node graph with Laplacian matrix")
    # Draw the 6-node graph on the left
    for b, (s, t, side) in BRANCHES6.items():
        x1, y1 = NODES6[s]
        x2, y2 = NODES6[t]
        svg += draw_edge_with_arrow_and_label(x1, y1, x2, y2, side=side, color=EDGE, width=3, directed=True, label=str(b))
    for name, (cx, cy) in NODES6.items():
        svg += node(cx, cy, label=name)

    # Laplacian table on the right
    table = [
        ["", "A", "B", "C", "D", "E", "F"],
        ["A", "3", "-2", "0", "-1", "0", "0"],
        ["B", "-2", "6", "-2", "-1", "-1", "0"],
        ["C", "0", "-2", "4", "0", "-1", "-1"],
        ["D", "-1", "-1", "0", "3", "-1", "0"],
        ["E", "0", "-1", "-1", "-1", "4", "-1"],
        ["F", "0", "0", "-1", "0", "-1", "2"],
    ]
    svg += f'<text x="540" y="50" text-anchor="start" font-family="sans-serif" font-size="18" fill="{TEXT}" font-weight="bold">L</text>'
    svg += draw_table(540, 70, table, cell_w=38, cell_h=32, font_size=13)
    svg += f'<text x="540" y="300" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">Parallel edges A–B and B–C</text>'
    svg += f'<text x="540" y="318" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">give off-diagonal values -2</text>'
    svg += svg_end()
    save_svg("fig-02-06-6-node-special-laplacian", svg)


# ============================================================
# Lecture 3 figures
# ============================================================


def fig_03_01_branch():
    svg = svg_start(500, 200, "A branch with current and voltage")
    svg += draw_edge_with_arrow_and_label(120, 100, 380, 100, directed=True)
    svg += node(120, 100, label="A")
    svg += node(380, 100, label="B")
    svg += subscript_text("i", "j", 250, 95, size=14, color=TEXT)
    svg += subscript_text("v", "j", 250, 80, size=14, color=TEXT)
    svg += f'<text x="250" y="140" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">branch j</text>'
    svg += svg_end()
    save_svg("fig-03-01-branch", svg)


def fig_03_02_twig_link():
    svg = svg_start(640, 240, "Twig and link in a spanning tree")
    svg += draw_edge_with_arrow_and_label(120, 120, 240, 60, color=TWIG, width=4, label="1")
    svg += draw_edge_with_arrow_and_label(240, 60, 240, 180, color=TWIG, width=4, label="2")
    svg += draw_edge_with_arrow_and_label(240, 180, 120, 120, color=LINK, width=3, label="3")
    svg += node(120, 120, label="A")
    svg += node(240, 60, label="B")
    svg += node(240, 180, label="C", ly=18)

    svg += f'<rect x="360" y="80" width="20" height="4" fill="{TWIG}"/>'
    svg += f'<text x="390" y="88" text-anchor="start" font-family="sans-serif" font-size="12" fill="{TEXT}">twig (in tree)</text>'
    svg += f'<rect x="360" y="110" width="20" height="4" fill="{LINK}"/>'
    svg += f'<text x="390" y="118" text-anchor="start" font-family="sans-serif" font-size="12" fill="{TEXT}">link (co-tree)</text>'
    svg += svg_end()
    save_svg("fig-03-02-twig-link", svg)


def fig_03_03_kcl():
    svg = svg_start(500, 260, "KCL at a node")
    svg += draw_edge_with_arrow_and_label(120, 60, 250, 120, directed=True, color="green")
    svg += draw_edge_with_arrow_and_label(120, 200, 250, 120, directed=True, color="green")
    svg += draw_edge_with_arrow_and_label(250, 120, 380, 60, directed=True, color="red")
    svg += draw_edge_with_arrow_and_label(250, 120, 380, 200, directed=True, color="red")
    svg += node(250, 120, label="A")
    svg += f'<text x="100" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" fill="green">in</text>'
    svg += f'<text x="100" y="210" text-anchor="middle" font-family="sans-serif" font-size="12" fill="green">in</text>'
    svg += f'<text x="400" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" fill="red">out</text>'
    svg += f'<text x="400" y="210" text-anchor="middle" font-family="sans-serif" font-size="12" fill="red">out</text>'
    svg += f'<text x="250" y="245" text-anchor="middle" font-family="sans-serif" font-size="14" fill="{TEXT}">Σ i</text>'
    svg += f'<text x="275" y="248" text-anchor="start" font-family="sans-serif" font-size="10" fill="{TEXT}">in</text>'
    svg += f'<text x="290" y="245" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TEXT}">= Σ i</text>'
    svg += f'<text x="330" y="248" text-anchor="start" font-family="sans-serif" font-size="10" fill="{TEXT}">out</text>'
    svg += svg_end()
    save_svg("fig-03-03-kcl", svg)


# ============================================================
# Lecture 4 figures
# ============================================================


def fig_04_01_cutset():
    svg = svg_start(640, 260, "A cutset divides a graph")
    svg += draw_edge_with_arrow_and_label(120, 130, 240, 70)
    svg += draw_edge_with_arrow_and_label(240, 70, 240, 190)
    svg += draw_edge_with_arrow_and_label(240, 190, 120, 130)
    svg += node(120, 130, label="A")
    svg += node(240, 70, label="B")
    svg += node(240, 190, label="C", ly=18)

    svg += f'<path d="M 180 20 Q 260 130 180 240" stroke="{CUTSET}" stroke-width="2" stroke-dasharray="6,4" fill="none"/>'
    svg += f'<text x="290" y="130" text-anchor="start" font-family="sans-serif" font-size="12" fill="{CUTSET}">cutset</text>'
    svg += f'<text x="80" y="130" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">part 1</text>'
    svg += f'<text x="300" y="130" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">part 2</text>'
    svg += svg_end()
    save_svg("fig-04-01-cutset", svg)


def fig_04_02_fundamental_cutset():
    svg = svg_start(640, 260, "Fundamental cutset for a twig")
    svg += draw_edge_with_arrow_and_label(120, 130, 240, 70, color=TWIG, width=4)
    svg += draw_edge_with_arrow_and_label(240, 70, 240, 190, color=TWIG, width=4, label="2")
    svg += draw_edge_with_arrow_and_label(240, 190, 120, 120, color=LINK, width=3, label="3")
    svg += node(120, 130, label="A")
    svg += node(240, 70, label="B")
    svg += node(240, 190, label="C", ly=18)

    svg += f'<line x1="200" y1="40" x2="280" y2="220" stroke="{CUTSET}" stroke-width="2" stroke-dasharray="6,4"/>'
    svg += f'<text x="300" y="130" text-anchor="start" font-family="sans-serif" font-size="12" fill="{CUTSET}">cut twig 2</text>'
    svg += f'<text x="80" y="130" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">{{A}}</text>'
    svg += f'<text x="300" y="80" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">{{B,C}}</text>'
    svg += svg_end()
    save_svg("fig-04-02-fundamental-cutset", svg)


def fig_04_03_cutset_matrix():
    svg = svg_start(640, 240, "Cutset matrix structure")
    # Title with subscript
    svg += f'<text x="105" y="35" text-anchor="start" font-family="sans-serif" font-size="16" fill="{TEXT}">= [</text>'
    svg += subscript_text("I", "n-1", 145, 35, size=16, color=TEXT)
    svg += f'<text x="178" y="35" text-anchor="start" font-family="sans-serif" font-size="16" fill="{TEXT}">|</text>'
    svg += subscript_text("Q", "f", 87, 35, size=16, color=TEXT)
    svg += subscript_text("Q", "l", 195, 35, size=16, color=TEXT)
    svg += f'<text x="218" y="35" text-anchor="start" font-family="sans-serif" font-size="16" fill="{TEXT}">]</text>'

    x0, y0 = 80, 60
    cell_w = 40
    cell_h = 24
    for i in range(5):
        for j in range(11):
            fill = "#edf2f7" if j < 5 and i == j else "#ffffff"
            svg += f'<rect x="{x0 + j*cell_w}" y="{y0 + i*cell_h}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="#cbd5e0" stroke-width="0.5"/>'
            if j < 5:
                val = 1 if i == j else 0
            else:
                val = "q"
            svg += plain_text(str(val), x0 + j*cell_w + cell_w/2, y0 + i*cell_h + cell_h/2 + 5, size=12, color=TEXT)

    svg += f'<text x="{x0 + 2*cell_w}" y="{y0 + 5*cell_h + 20}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">twigs</text>'
    svg += f'<text x="{x0 + 8*cell_w}" y="{y0 + 5*cell_h + 20}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">links</text>'
    svg += svg_end()
    save_svg("fig-04-03-cutset-matrix", svg)


# ============================================================
# Lecture 5 figures
# ============================================================

NODES6 = {
    'A': (180, 120),
    'B': (180, 280),
    'C': (180, 440),
    'D': (460, 120),
    'E': (460, 280),
    'F': (460, 440),
}

BRANCHES6 = {
    1: ('B', 'A', 1),
    2: ('C', 'B', 1),
    3: ('A', 'B', -1),
    4: ('B', 'C', -1),
    5: ('D', 'A', 0),
    6: ('B', 'D', 0),
    7: ('E', 'B', 0),
    8: ('C', 'E', 0),
    9: ('C', 'F', 0),
    10: ('D', 'E', 0),
    12: ('E', 'F', 0),
}


def draw_6_node_graph(selected=None, cutset=None, partition=None, highlight_edge=None):
    """Return SVG fragments for the 6-node 11-branch graph."""
    fragments = []
    selected = set(selected or [])
    for b, (s, t, side) in BRANCHES6.items():
        x1, y1 = NODES6[s]
        x2, y2 = NODES6[t]
        if b in selected:
            color = TWIG
            width = 4
        else:
            color = EDGE
            width = 3
        if highlight_edge == b:
            color = CUTSET
            width = 5
        fragments.append(draw_edge_with_arrow_and_label(x1, y1, x2, y2, side=side, color=color, width=width,
                                                        directed=True, label=str(b)))
    # Partition shading
    if partition:
        for name, (cx, cy) in NODES6.items():
            fill = "#bee3f8" if name in partition[0] else "#feebc8"
            fragments.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="{fill}" opacity="0.5"/>')
    # Nodes on top
    for name, (cx, cy) in NODES6.items():
        fragments.append(node(cx, cy, label=name))
    # Cutset label
    if cutset:
        fragments.append(f'<text x="320" y="30" text-anchor="middle" font-family="sans-serif" font-size="14" fill="{CUTSET}" font-weight="bold">{cutset}</text>')
    return "".join(fragments)


def fig_05_01_full_6_node_11_branch():
    svg = svg_start(640, 560, "Full 6 node 11 branch graph")
    svg += draw_6_node_graph()
    svg += svg_end()
    save_svg("fig-05-01-full-6-node-11-branch", svg)


def fig_05_02_tree_t0():
    svg = svg_start(640, 560, "Spanning tree T0")
    fragments = []
    for b in [1, 2, 5, 10, 12]:
        s, t, side = BRANCHES6[b]
        x1, y1 = NODES6[s]
        x2, y2 = NODES6[t]
        fragments.append(draw_edge_with_arrow_and_label(x1, y1, x2, y2, side=side, color=TWIG, width=4,
                                                        directed=True, label=str(b)))
    for name, (cx, cy) in NODES6.items():
        fragments.append(node(cx, cy, label=name))
    svg += "".join(fragments)
    svg += subscript_text("T", "0", 85, 35, size=14, color=TWIG, font_weight="bold")
    svg += f'<text x="100" y="35" text-anchor="start" font-family="sans-serif" font-size="14" fill="{TWIG}">= {{1, 2, 5, 10, 12}}</text>'
    svg += svg_end()
    save_svg("fig-05-02-tree-t0", svg)


def fig_05_03_cutset_c1():
    svg = svg_start(640, 560, "Cutset C1 for twig 1")
    svg += draw_6_node_graph(selected=[1, 2, 5, 10, 12], cutset="C1: cut twig 1 (B→A)",
                            partition=[{'B','C'}, {'A','D','E','F'}], highlight_edge=1)
    svg += f'<text x="320" y="540" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">Crossing edges: {{1, 3, 6, 7, 8, 9}}</text>'
    svg += svg_end()
    save_svg("fig-05-03-cutset-c1", svg)


def fig_05_04_cutset_c2():
    svg = svg_start(640, 560, "Cutset C2 for twig 5")
    svg += draw_6_node_graph(selected=[1, 2, 5, 10, 12], cutset="C2: cut twig 5 (D→A)",
                            partition=[{'D','E','F'}, {'A','B','C'}], highlight_edge=5)
    svg += f'<text x="320" y="540" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">Crossing edges: {{5, 6, 7, 8, 9}}</text>'
    svg += svg_end()
    save_svg("fig-05-04-cutset-c2", svg)


def fig_05_05_cutset_c3():
    svg = svg_start(640, 560, "Cutset C3 for twig 2")
    svg += draw_6_node_graph(selected=[1, 2, 5, 10, 12], cutset="C3: cut twig 2 (C→B)",
                            partition=[{'C'}, {'A','B','D','E','F'}], highlight_edge=2)
    svg += f'<text x="320" y="540" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">Crossing edges: {{2, 4, 8, 9}}</text>'
    svg += svg_end()
    save_svg("fig-05-05-cutset-c3", svg)


def fig_05_06_cutset_c4():
    svg = svg_start(640, 560, "Cutset C4 for twig 10")
    svg += draw_6_node_graph(selected=[1, 2, 5, 10, 12], cutset="C4: cut twig 10 (D→E)",
                            partition=[{'D'}, {'A','B','C','E','F'}], highlight_edge=10)
    svg += f'<text x="320" y="540" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">Crossing edges: {{7, 8, 9, 10}}</text>'
    svg += svg_end()
    save_svg("fig-05-06-cutset-c4", svg)


def fig_05_07_cutset_c5():
    svg = svg_start(640, 560, "Cutset C5 for twig 12")
    svg += draw_6_node_graph(selected=[1, 2, 5, 10, 12], cutset="C5: cut twig 12 (E→F)",
                            partition=[{'F'}, {'A','B','C','D','E'}], highlight_edge=12)
    svg += f'<text x="320" y="540" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{TEXT}">Crossing edges: {{9, 12}}</text>'
    svg += svg_end()
    save_svg("fig-05-07-cutset-c5", svg)


# ============================================================
# Lecture 6 figures
# ============================================================


def fig_06_01_cutset_matrix_qf():
    svg = svg_start(640, 320, "Cutset matrix Qf")
    # Header
    svg += subscript_text("Q", "f", 65, 40, size=18, color=TEXT)
    svg += f'<text x="60" y="65" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">twigs: 1 5 2 10 12</text>'
    svg += f'<text x="60" y="82" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">links: 3 4 6 7 8 9</text>'

    data = [
        [1, 0, 0, 0, 0, -1, 0, 1, -1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, -1, 1, -1, -1],
        [0, 0, 1, 0, 0, 0, -1, 0, 0, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0, -1, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    ]
    x0, y0 = 60, 100
    cell_w = 42
    cell_h = 26
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            fill = "#bee3f8" if j < 5 and i == j else "#ffffff"
            svg += f'<rect x="{x0 + j*cell_w}" y="{y0 + i*cell_h}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="#cbd5e0" stroke-width="0.5"/>'
            svg += plain_text(str(val), x0 + j*cell_w + cell_w/2, y0 + i*cell_h + cell_h/2 + 5, size=12, color=TEXT)

    # Labels
    svg += subscript_text("C", "1", x0 - 25, y0 + 2.5*cell_h, size=14, color=TEXT)
    svg += f'<text x="{x0 - 25}" y="{y0 + 3.5*cell_h}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{LIGHT}">...</text>'
    svg += subscript_text("I", "5", x0 + 5*cell_w + 20, y0 - 15, size=14, color=TEXT)
    svg += subscript_text("Q", "l", x0 + 8*cell_w, y0 - 15, size=14, color=TEXT)
    svg += f'<text x="60" y="250" text-anchor="start" font-family="sans-serif" font-size="12" fill="{LIGHT}">Identity block proves linear independence</text>'
    svg += svg_end()
    save_svg("fig-06-01-cutset-matrix-qf", svg)


if __name__ == "__main__":
    fig_01_01_graph_abc()
    fig_01_02_directed_graph()
    fig_01_03_connected_disconnected()
    fig_01_04_cycle()
    fig_01_05_tree()
    fig_01_06_spanning_trees_triangle()

    fig_02_01_incidence_matrix()
    fig_02_02_laplacian_matrix()
    fig_02_03_matrix_tree_theorem()
    fig_02_04_6_node_special_laplacian()

    fig_03_01_branch()
    fig_03_02_twig_link()
    fig_03_03_kcl()

    fig_04_01_cutset()
    fig_04_02_fundamental_cutset()
    fig_04_03_cutset_matrix()

    fig_05_01_full_6_node_11_branch()
    fig_05_02_tree_t0()
    fig_05_03_cutset_c1()
    fig_05_04_cutset_c2()
    fig_05_05_cutset_c3()
    fig_05_06_cutset_c4()
    fig_05_07_cutset_c5()

    fig_06_01_cutset_matrix_qf()

    print("\nAll figures generated.")
