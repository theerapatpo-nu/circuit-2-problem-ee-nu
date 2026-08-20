#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""สร้าง SVG ประกอบเฉลยโจทย์ [4.4] ด้วย Python standard library เท่านั้น

รันจากโฟลเดอร์ 4.4:
    python3 assets/make_figures.py

ผลลัพธ์:
    assets/fig-01-topology-duality.svg
    assets/fig-02-circuit-anatomy.svg
    assets/fig-03-tree-tieset.svg
    assets/fig-04-branch-models.svg
    assets/fig-05-matrix-solve.svg
    assets/fig-06-symbolic-results.svg
    assets/fig-07-independent-checks.svg
    assets/fig-08-numeric-power.svg
"""

from __future__ import annotations

import html
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent

INK = "#172033"
MUTED = "#64748b"
GRID = "#dbe3ee"
SOFT = "#f8fafc"
PAPER = "#ffffff"
LINK = "#dc2626"
TWIG = "#111827"
BLUE = "#2563eb"
GREEN = "#059669"
PURPLE = "#7c3aed"
AMBER = "#b45309"
CYAN = "#0891b2"

FONT = "'Sarabun','Noto Sans Thai','IBM Plex Sans Thai','Segoe UI',sans-serif"
MATH = "'STIX Two Math','Cambria Math','Times New Roman',serif"

MARKERS = {
    INK: "ink",
    LINK: "red",
    BLUE: "blue",
    GREEN: "green",
    PURPLE: "purple",
    AMBER: "amber",
    CYAN: "cyan",
    TWIG: "black",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def head(width: int, height: int, title: str) -> str:
    marker_defs = []
    for color, name in MARKERS.items():
        marker_defs.append(
            f'<marker id="arr-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{color}"/></marker>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{esc(title)}" '
        f'font-family="{FONT}">\n<title>{esc(title)}</title>\n<defs>'
        + "".join(marker_defs)
        + f'</defs>\n<rect width="{width}" height="{height}" fill="{PAPER}"/>\n'
    )


def tail() -> str:
    return "</svg>\n"


def text(
    x: float,
    y: float,
    value: object,
    size: float = 16,
    color: str = INK,
    anchor: str = "middle",
    weight: int = 400,
    family: str | None = None,
    italic: bool = False,
) -> str:
    style = "italic" if italic else "normal"
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" '
        f'font-family="{family or FONT}">{esc(value)}</text>\n'
    )


def multiline(
    x: float,
    y: float,
    lines: list[str],
    size: float = 15,
    color: str = INK,
    anchor: str = "start",
    gap: float = 25,
    weight: int = 400,
    family: str | None = None,
) -> str:
    out = []
    for index, value in enumerate(lines):
        out.append(text(x, y + index * gap, value, size, color, anchor, weight, family))
    return "".join(out)


def math_text(x: float, y: float, value: object, size: float = 18, color: str = INK,
              anchor: str = "middle", weight: int = 400) -> str:
    return text(x, y, value, size, color, anchor, weight, MATH, True)


def line(x1: float, y1: float, x2: float, y2: float, color: str = INK,
         width: float = 2.6, dash: str | None = None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>\n'
    )


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = INK,
          width: float = 2.6, dash: str | None = None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    marker = MARKERS.get(color, "ink")
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
        f'marker-end="url(#arr-{marker})"{d}/>\n'
    )


def path(d: str, color: str = INK, width: float = 2.6, fill: str = "none",
         dash: str | None = None, arrow_end: bool = False) -> str:
    da = f' stroke-dasharray="{dash}"' if dash else ""
    marker = f' marker-end="url(#arr-{MARKERS.get(color, "ink")})"' if arrow_end else ""
    return (
        f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round"{da}{marker}/>\n'
    )


def rect(x: float, y: float, width: float, height: float, fill: str = PAPER,
         stroke: str = GRID, radius: float = 14, stroke_width: float = 1.5,
         dash: str | None = None) -> str:
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{da}/>\n'
    )


def circle(cx: float, cy: float, radius: float, fill: str = PAPER,
           stroke: str = INK, stroke_width: float = 2.4, dash: str | None = None) -> str:
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{radius:.1f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}"{da}/>\n'
    )


def node(x: float, y: float, label: str | None = None, dx: float = 0, dy: float = -14) -> str:
    out = circle(x, y, 6.5, INK, INK, 1)
    if label:
        out += math_text(x + dx, y + dy, label, 18, INK, "middle", 700)
    return out


def panel_title(x: float, y: float, number: str, title: str, color: str = BLUE) -> str:
    return (
        circle(x, y - 5, 15, color, color, 1)
        + text(x, y, number, 14, PAPER, "middle", 700)
        + text(x + 26, y, title, 16, INK, "start", 700)
    )


def resistor_points(x1: float, y1: float, x2: float, y2: float,
                    amplitude: float = 10, turns: int = 6) -> str:
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    points = [(x1, y1)]
    for k in range(1, turns * 2):
        distance = length * k / (turns * 2)
        sign = 1 if k % 2 else -1
        points.append((x1 + ux * distance + px * amplitude * sign,
                       y1 + uy * distance + py * amplitude * sign))
    points.append((x2, y2))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def resistor(x1: float, y1: float, x2: float, y2: float, label: str | None = None,
             color: str = INK, label_dx: float = 0, label_dy: float = -17) -> str:
    out = (
        f'<polyline points="{resistor_points(x1, y1, x2, y2)}" fill="none" '
        f'stroke="{color}" stroke-width="2.7" stroke-linejoin="round" '
        f'stroke-linecap="round"/>\n'
    )
    if label:
        out += math_text((x1 + x2) / 2 + label_dx, (y1 + y2) / 2 + label_dy,
                         label, 18, color)
    return out


def voltage_source(cx: float, cy: float, radius: float = 25, label: str = "v_s") -> str:
    return (
        circle(cx, cy, radius, PAPER, PURPLE, 2.6)
        + line(cx - 7, cy - 9, cx + 7, cy - 9, PURPLE, 2.2)
        + line(cx, cy - 16, cx, cy - 2, PURPLE, 2.2)
        + line(cx - 7, cy + 10, cx + 7, cy + 10, PURPLE, 2.2)
        + math_text(cx - 42, cy + 6, label, 18, PURPLE, "end", 700)
    )


def current_source(cx: float, cy: float, orientation: str = "up",
                   label: str = "i_s", label_dx: float = 40, label_dy: float = 6) -> str:
    out = circle(cx, cy, 25, PAPER, CYAN, 2.6)
    if orientation == "up":
        out += arrow(cx, cy + 13, cx, cy - 13, CYAN, 2.5)
    elif orientation == "left":
        out += arrow(cx + 13, cy, cx - 13, cy, CYAN, 2.5)
    elif orientation == "right":
        out += arrow(cx - 13, cy, cx + 13, cy, CYAN, 2.5)
    else:
        out += arrow(cx, cy - 13, cx, cy + 13, CYAN, 2.5)
    out += math_text(cx + label_dx, cy + label_dy, label, 18, CYAN, "start", 700)
    return out


def title_block(width: int, title: str, subtitle: str) -> str:
    return (
        text(width / 2, 38, title, 21, INK, "middle", 700)
        + text(width / 2, 64, subtitle, 14, MUTED)
    )


def save(filename: str, body: str) -> None:
    target = OUT / filename
    target.write_text(body, encoding="utf-8")
    print(f"wrote {target.name}")


def triangle_graph(cx: float, cy: float, scale: float = 1.0, labels: bool = True,
                   loop: bool = True) -> str:
    a = (cx - 145 * scale, cy - 92 * scale)
    b = (cx + 145 * scale, cy - 92 * scale)
    o = (cx, cy + 145 * scale)
    out = path(f"M {o[0]} {o[1]} L {a[0]} {a[1]}", TWIG, 7)
    out += path(f"M {b[0]} {b[1]} L {a[0]} {a[1]}", TWIG, 7)
    out += path(f"M {o[0]} {o[1]} L {b[0]} {b[1]}", LINK, 3.5)
    # Branch reference arrows: 1 O->B, 2 B->A, 3 O->A.
    out += arrow(o[0] + 35 * scale, o[1] - 57 * scale,
                 o[0] + 76 * scale, o[1] - 124 * scale, LINK, 2.8)
    out += arrow(cx + 38 * scale, a[1], cx - 38 * scale, a[1], TWIG, 2.8)
    out += arrow(o[0] - 35 * scale, o[1] - 57 * scale,
                 o[0] - 76 * scale, o[1] - 124 * scale, TWIG, 2.8)
    out += node(*a, "A", -14 * scale, -18 * scale)
    out += node(*b, "B", 14 * scale, -18 * scale)
    out += node(*o, "O", 0, 30 * scale)
    if labels:
        out += text(cx + 108 * scale, cy + 18 * scale, "1", 22, LINK, "middle", 700)
        out += text(cx, a[1] - 15 * scale, "2", 22, TWIG, "middle", 700)
        out += text(cx - 108 * scale, cy + 18 * scale, "3", 22, TWIG, "middle", 700)
    if loop:
        out += path(
            f"M {o[0]+12*scale} {o[1]-30*scale} "
            f"L {b[0]-22*scale} {b[1]+12*scale} "
            f"L {a[0]+22*scale} {a[1]+12*scale} "
            f"L {o[0]-12*scale} {o[1]-30*scale}",
            LINK, 2.2, "none", "8 7", True,
        )
        out += math_text(cx + 6 * scale, cy + 28 * scale, "j₁", 20, LINK, "middle", 700)
    return out


def fig01() -> None:
    width, height = 1040, 730
    out = head(width, height, "ความสมมาตรระหว่าง tie-set และ cut-set")
    out += title_block(width, "รูปที่ 1 — โทโพโลยีหนึ่งชุด มองได้จาก cycle space และ cut space",
                       "วงรอบสร้างจากลิงก์ • ชุดตัดสร้างจากทวิก • สองปริภูมิตั้งฉากกัน")
    out += triangle_graph(270, 300, 0.88)

    out += rect(515, 92, 475, 245, "#eff6ff", BLUE)
    out += panel_title(544, 128, "B", "Loop / Fundamental tie-set", BLUE)
    out += multiline(544, 166, [
        "เติมลิงก์ 1 กลับลงในทรี T={2,3}",
        "ได้วงรอบ O → B → A → O",
        "จำนวนตัวแปรอิสระ l=b−n+1=1",
    ], 14, MUTED, "start", 27)
    out += math_text(752, 270, "B = [ 1   1   −1 ]", 24, BLUE, "middle", 700)
    out += math_text(752, 308, "Bv = 0  •  i = Bᵀj", 19, INK, "middle", 600)

    out += rect(515, 360, 475, 245, "#ecfdf5", GREEN)
    out += panel_title(544, 396, "Q", "Cut-set / Fundamental cut-set", GREEN)
    out += multiline(544, 434, [
        "ตัดทวิก 2 และ 3 ออกจากทรีทีละกิ่ง",
        "ได้ชุดตัดอิสระ 2 ชุด",
        "จำนวนตัวแปรแรงดันทวิก n−1=2",
    ], 14, MUTED, "start", 27)
    out += math_text(752, 538, "Q = [ −1  1  0 ;  1  0  1 ]", 22, GREEN, "middle", 700)
    out += math_text(752, 576, "Qi = 0  •  v = Q^T e_t", 19, INK, "middle", 600)

    out += rect(75, 618, 890, 78, "#fff7ed", AMBER, 12, 1.8)
    out += math_text(width / 2, 654, "B Qᵀ = 0", 25, AMBER, "middle", 700)
    out += text(width / 2, 681, "cycle space ⟂ cut space — รากฐานของ KVL, KCL และ Tellegen", 14, MUTED)
    out += tail()
    save("fig-01-topology-duality.svg", out)


def fig02() -> None:
    width, height = 1040, 790
    out = head(width, height, "กายวิภาควงจรและกิ่งประกอบ")
    out += title_block(width, "รูปที่ 2 — จากวงจรจริงสู่กราฟกิ่งประกอบ 3 กิ่ง",
                       "ระบุปม A, B, O • แยกกิ่ง Thévenin/Norton • ยึดทิศอ้างอิงจากรูปทรี")

    # Composite branch callouts are drawn first so the circuit remains visible above them.
    xa, xb, xo, ytop, ybot = 380, 680, 120, 230, 500
    out += rect(72, 178, 275, 365, "#faf5ff", PURPLE, 16, 2, "8 6")
    out += rect(355, 95, 350, 178, "#ecfeff", CYAN, 16, 2, "8 6")
    out += rect(650, 205, 185, 330, "#eff6ff", BLUE, 16, 2, "8 6")

    # Physical circuit.
    out += line(xo, ybot, 800, ybot)
    out += line(xo, ybot, xo, 390)
    out += voltage_source(xo, 365)
    out += line(xo, 340, xo, ytop)
    out += resistor(xo, ytop, 300, ytop, "R₁")
    out += line(300, ytop, xa, ytop)
    out += resistor(xa, ytop, xb, ytop, "R₂")
    out += line(xb, ytop, xb, 300)
    out += resistor(xb, 300, xb, 430, "R₃", INK, 35, 0)
    out += line(xb, 430, xb, ybot)
    # Top current source.
    out += line(xa, ytop, xa, 130)
    out += line(xa, 130, 505, 130)
    out += current_source(530, 130, "left", "i_s", -5, -38)
    out += line(555, 130, xb, 130)
    out += line(xb, 130, xb, ytop)
    # Right current source.
    out += line(xb, ytop, 800, ytop)
    out += line(800, ytop, 800, 340)
    out += current_source(800, 365, "up", "i_s", 42, 7)
    out += line(800, 390, 800, ybot)
    out += node(xa, ytop, "A", 0, -20)
    out += node(xb, ytop, "B", 0, -20)
    out += node(500, ybot, "O", 0, 28)

    # Composite branch labels.
    out += text(88, 570, "กิ่ง 3: v_s อนุกรม R₁", 15, PURPLE, "start", 700)
    out += text(88, 594, "Thévenin • O → A", 13.5, MUTED, "start")
    out += text(370, 295, "กิ่ง 2: i_s ขนาน R₂", 15, CYAN, "start", 700)
    out += text(370, 319, "Norton • B → A", 13.5, MUTED, "start")
    out += text(660, 570, "กิ่ง 1: i_s ขนาน R₃", 15, BLUE, "start", 700)
    out += text(660, 594, "Norton • O → B", 13.5, MUTED, "start")

    out += arrow(900, 360, 960, 360, MUTED, 2.4)
    out += text(930, 338, "ยุบเป็น", 13, MUTED)
    out += triangle_graph(895, 620, 0.32, True, False)

    out += rect(75, 650, 720, 105, SOFT, GRID)
    out += text(96, 680, "แรงดันกิ่งแบบ associated reference direction", 15, INK, "start", 700)
    out += math_text(96, 716, "v₁ = V_O−V_B  •  v₂ = V_B−V_A  •  v₃ = V_O−V_A", 19, INK, "start")
    out += text(96, 742, "ขั้ว + อยู่ที่หางลูกศรของทุกกิ่ง", 13.5, MUTED, "start")
    out += tail()
    save("fig-02-circuit-anatomy.svg", out)


def fig03() -> None:
    width, height = 1040, 690
    out = head(width, height, "ทรี ลิงก์ และเมทริกซ์ tie-set")
    out += title_block(width, "รูปที่ 3 — เดินวงรอบหลักมูลเพื่อสร้าง B",
                       "ทิศวงรอบยึดตามลิงก์ 1: O → B → A → O")
    out += triangle_graph(280, 310, 1.05)

    out += rect(540, 100, 440, 300, PAPER, GRID)
    out += text(564, 136, "ตารางเก็บเครื่องหมาย", 17, INK, "start", 700)
    rows = [
        ("กิ่ง", "ทิศเดิน j₁", "เทียบลูกศร", "b_1k"),
        ("1", "O → B", "ตาม", "+1"),
        ("2", "B → A", "ตาม", "+1"),
        ("3", "A → O", "สวน", "−1"),
    ]
    yy = 165
    for ridx, row in enumerate(rows):
        fill = "#eef2ff" if ridx == 0 else ("#ffffff" if ridx % 2 else SOFT)
        out += rect(558, yy + ridx * 44, 404, 42, fill, GRID, 0, 1)
        xs = [588, 690, 820, 930]
        for x, cell in zip(xs, row):
            out += text(x, yy + 27 + ridx * 44, cell, 14.5,
                        "#3730a3" if ridx == 0 else INK,
                        "middle", 700 if ridx == 0 else 500)

    out += rect(540, 430, 440, 215, "#fff7ed", AMBER)
    out += text(564, 466, "ผลลัพธ์เชิงโทโพโลยี", 17, AMBER, "start", 700)
    out += math_text(760, 510, "B = [ 1   1   −1 ]", 25, INK, "middle", 700)
    out += math_text(760, 550, "i = Bᵀj  ⇒  i₁=i₂=j₁, i₃=−j₁", 19, INK, "middle")
    out += math_text(760, 592, "Bv = 0  ⇒  v₁+v₂−v₃=0", 19, INK, "middle")
    out += text(760, 625, "ทุกบรรทัดยังไม่ใช้ค่า R, v_s หรือ i_s", 13.5, MUTED)
    out += tail()
    save("fig-03-tree-tieset.svg", out)


def branch_icon(x: float, y_top: float, y_bottom: float, kind: str, resistor_label: str,
                branch_color: str, source_label: str) -> str:
    out = node(x, y_top)
    out += node(x, y_bottom)
    if kind == "thevenin":
        out += line(x, y_bottom, x, y_bottom - 42)
        out += voltage_source(x, y_bottom - 68, 24, source_label)
        out += line(x, y_bottom - 92, x, y_top + 92)
        out += resistor(x, y_top + 92, x, y_top + 34, resistor_label,
                        INK, 38, 2)
        out += line(x, y_top + 34, x, y_top)
    else:
        left, right = x - 55, x + 55
        out += line(left, y_top, right, y_top)
        out += line(left, y_bottom, right, y_bottom)
        out += line(left, y_bottom, left, y_bottom - 88)
        out += current_source(left, (y_top + y_bottom) / 2, "up", source_label, 34, 6)
        out += line(left, y_top + 88, left, y_top)
        out += line(right, y_bottom, right, y_bottom - 50)
        out += resistor(right, y_bottom - 50, right, y_top + 50, resistor_label,
                        INK, 36, 4)
        out += line(right, y_top + 50, right, y_top)
    out += arrow(x - 92, y_bottom - 15, x - 92, y_top + 15, branch_color, 2.5)
    out += text(x - 105, (y_top + y_bottom) / 2 + 6, "i_k", 16, branch_color, "end", 700)
    out += text(x + 92, y_bottom - 18, "+", 22, branch_color, "middle", 700)
    out += text(x + 92, y_top + 28, "−", 22, branch_color, "middle", 700)
    return out


def fig04() -> None:
    width, height = 1040, 720
    out = head(width, height, "สมการเฉพาะกิ่ง")
    out += title_block(width, "รูปที่ 4 — สมการเฉพาะกิ่งของ Norton, Norton และ Thévenin",
                       "เขียนแรงดันกิ่งเป็นฟังก์ชันของกระแสกิ่งก่อนประกอบสมการเมทริกซ์")
    panels = [
        (30, BLUE, "#eff6ff", "กิ่ง 1 • O → B", "Norton: i_s ∥ R₃",
         "v₁ = R₃(i₁−i_s)", "norton", "R₃", "i_s"),
        (365, CYAN, "#ecfeff", "กิ่ง 2 • B → A", "Norton: i_s ∥ R₂",
         "v₂ = R₂(i₂−i_s)", "norton", "R₂", "i_s"),
        (700, PURPLE, "#faf5ff", "กิ่ง 3 • O → A", "Thévenin: v_s + R₁",
         "v₃ = R₁i₃−v_s", "thevenin", "R₁", "v_s"),
    ]
    for x, color, bg, title, subtitle, formula, kind, resistor_label, source_label in panels:
        out += rect(x, 95, 310, 580, bg, color)
        out += text(x + 20, 128, title, 16, color, "start", 700)
        out += text(x + 20, 153, subtitle, 14, MUTED, "start")
        out += branch_icon(x + 155, 205, 485, kind, resistor_label, color, source_label)
        if kind == "norton":
            out += text(x + 155, 520, "i_R = i_k − i_s", 15, MUTED)
        else:
            out += text(x + 155, 520, "แหล่งจ่ายยกศักย์ +v_s ตามทิศกิ่ง", 14, MUTED)
        out += rect(x + 18, 555, 274, 72, PAPER, color, 10, 1.5)
        out += math_text(x + 155, 598, formula, 21, color, "middle", 700)
        out += text(x + 155, 652, "ขั้ว + ของ v_k อยู่ที่หางลูกศร", 12.5, MUTED)
    out += tail()
    save("fig-04-branch-models.svg", out)


def fig05() -> None:
    width, height = 1040, 730
    out = head(width, height, "การประกอบและแก้สมการวงรอบแบบเมทริกซ์")
    out += title_block(width, "รูปที่ 5 — จากสมการกิ่งสู่ B Z_b Bᵀ j",
                       "ประกอบทีละก้อนเพื่อลดความผิดพลาดเรื่องเครื่องหมายของแหล่งจ่าย")

    steps = [
        ("1", "สมการกิ่ง", "v = Z_b i + v_sb − Z_b i_sb", BLUE, "#eff6ff"),
        ("2", "แทนข้อบังคับโทโพโลยี", "Bv=0  และ  i=Bᵀj", GREEN, "#ecfdf5"),
        ("3", "ย้ายพจน์แหล่งจ่าย", "B Z_b Bᵀ j = B Z_b i_sb − B v_sb", PURPLE, "#faf5ff"),
    ]
    y = 102
    for number, cap, formula, color, bg in steps:
        out += rect(70, y, 900, 105, bg, color)
        out += circle(108, y + 52, 22, color, color, 1)
        out += text(108, y + 59, number, 18, PAPER, "middle", 700)
        out += text(148, y + 37, cap, 15, color, "start", 700)
        out += math_text(520, y + 75, formula, 21, INK, "middle", 600)
        y += 125

    out += rect(70, 488, 280, 150, PAPER, GRID)
    out += text(90, 520, "Loop impedance", 15, BLUE, "start", 700)
    out += math_text(210, 562, "B Z_b Bᵀ = R_T", 20, INK)
    out += text(210, 598, "R_T = R₁+R₂+R₃", 14, MUTED)

    out += rect(380, 488, 280, 150, PAPER, GRID)
    out += text(400, 520, "Norton drive", 15, CYAN, "start", 700)
    out += math_text(520, 562, "B Z_b i_sb", 20, INK)
    out += math_text(520, 598, "= (R₂+R₃)i_s", 17, MUTED)

    out += rect(690, 488, 280, 150, PAPER, GRID)
    out += text(710, 520, "Thévenin drive", 15, PURPLE, "start", 700)
    out += math_text(830, 562, "−B v_sb", 20, INK)
    out += math_text(830, 598, "= −v_s", 17, MUTED)

    out += rect(150, 658, 740, 52, "#fff7ed", AMBER, 10, 2)
    out += math_text(520, 692, "R_T j₁ = (R₂+R₃)i_s − v_s", 23, AMBER, "middle", 700)
    out += tail()
    save("fig-05-matrix-solve.svg", out)


def fig06() -> None:
    width, height = 1040, 760
    out = head(width, height, "คำตอบเชิงสัญลักษณ์")
    out += title_block(width, "รูปที่ 6 — คำตอบครบทุกกระแสกิ่งและแรงดันกิ่ง",
                       "ให้ R_T=R₁+R₂+R₃ และ K=v_s+R₁i_s")
    out += triangle_graph(285, 310, 1.05)

    out += rect(540, 92, 440, 305, PAPER, GRID)
    out += text(565, 128, "กระแส", 17, BLUE, "start", 700)
    out += math_text(760, 172, "j₁ = [(R₂+R₃)i_s−v_s] / R_T", 20, LINK, "middle", 700)
    out += math_text(760, 222, "i₁ = i₂ = j₁", 21, INK, "middle", 600)
    out += math_text(760, 272, "i₃ = −j₁", 21, INK, "middle", 600)
    out += rect(574, 308, 372, 58, "#eff6ff", BLUE, 9, 1.4)
    out += text(760, 343, "ค่าลบ = ไหลจริงสวนลูกศรอ้างอิง", 14, BLUE, "middle", 700)

    out += rect(540, 420, 440, 285, PAPER, GRID)
    out += text(565, 456, "แรงดัน", 17, GREEN, "start", 700)
    out += math_text(760, 504, "v₁ = −R₃K / R_T", 21, INK, "middle", 600)
    out += math_text(760, 548, "v₂ = −R₂K / R_T", 21, INK, "middle", 600)
    out += math_text(760, 592, "v₃ = −(R₂+R₃)K / R_T", 21, INK, "middle", 600)
    out += math_text(760, 648, "v₁ + v₂ − v₃ = 0  ✓", 20, GREEN, "middle", 700)
    out += text(760, 682, "V_B=−v₁ • V_A=−v₃", 14, MUTED)

    out += rect(60, 590, 440, 115, "#fff7ed", AMBER)
    out += text(82, 622, "กระแสระดับองค์ประกอบ", 15, AMBER, "start", 700)
    out += math_text(280, 660, "i_R₂ = i_R₃ = −K / R_T", 20, INK)
    out += text(280, 688, "เมื่อ K>0 กระแสจริงไหล A → B → O", 13.5, MUTED)
    out += tail()
    save("fig-06-symbolic-results.svg", out)


def fig07() -> None:
    width, height = 1040, 720
    out = head(width, height, "การตรวจคำตอบอิสระสี่ทาง")
    out += title_block(width, "รูปที่ 7 — การตรวจคำตอบอิสระ 4 ทาง",
                       "KCL • Mesh constraints • พฤติกรรมขีดจำกัด • Tellegen")
    cards = [
        (45, 100, BLUE, "#eff6ff", "1", "Node Analysis", [
            "(V_A−v_s)/R₁ + (V_A−V_B)/R₂ = i_s",
            "(V_B−V_A)/R₂ + V_B/R₃ = 0",
            "⇒ V_A=(R₂+R₃)K/R_T",
        ]),
        (530, 100, PURPLE, "#faf5ff", "2", "Mesh / Supermesh", [
            "m₂=m₃=−i_s",
            "−v_s+R₁m₀+(R₂+R₃)(m₀+i_s)=0",
            "⇒ m₀=i₃=−j₁",
        ]),
        (45, 390, AMBER, "#fff7ed", "3", "Limiting Cases", [
            "i_s=0  ⇒  i₃=v_s/R_T",
            "R₁→0  ⇒  V_A→v_s",
            "v_s=(R₂+R₃)i_s  ⇒  j₁=0",
        ]),
        (530, 390, GREEN, "#ecfdf5", "4", "Tellegen / Power", [
            "vᵀi = vᵀBᵀj",
            "= (Bv)ᵀj = 0",
            "กำลังดูดกลืนรวม = กำลังจ่ายรวม",
        ]),
    ]
    for x, y, color, bg, number, cap, lines_ in cards:
        out += rect(x, y, 465, 250, bg, color)
        out += panel_title(x + 30, y + 42, number, cap, color)
        out += line(x + 22, y + 68, x + 443, y + 68, color, 1.2)
        for idx, value in enumerate(lines_):
            out += math_text(x + 232, y + 112 + idx * 46, value, 17.5, INK,
                             "middle", 500 if idx < 2 else 700)
        out += text(x + 420, y + 228, "✓", 24, color, "middle", 700)
    out += tail()
    save("fig-07-independent-checks.svg", out)


def fig08() -> None:
    width, height = 1040, 810
    out = head(width, height, "ตัวอย่างตัวเลขและสมดุลกำลัง")
    out += title_block(width, "รูปที่ 8 — ตัวอย่างตัวเลขและ Tellegen power balance",
                       "R₁=2 Ω • R₂=3 Ω • R₃=5 Ω • v_s=10 V • i_s=4 A")

    out += triangle_graph(250, 275, 0.85)
    out += text(250, 80, "R_T=10 Ω • K=18 V", 15, MUTED)
    out += math_text(250, 486, "j₁=2.2 A", 23, LINK, "middle", 700)
    out += math_text(250, 526, "i₁=i₂=2.2 A  •  i₃=−2.2 A", 17.5, INK)
    out += math_text(250, 562, "v₁=−9 V  •  v₂=−5.4 V  •  v₃=−14.4 V", 17.5, INK)
    out += text(250, 592, "KVL: −9−5.4−(−14.4)=0 ✓", 14.5, GREEN, "middle", 700)

    out += rect(500, 95, 490, 245, PAPER, GRID)
    out += text(525, 130, "แรงดันปมและ KCL", 17, BLUE, "start", 700)
    out += math_text(745, 178, "V_A=14.4 V   V_B=9.0 V", 20, INK, "middle", 600)
    out += text(525, 222, "ที่ A: (14.4−10)/2 + (14.4−9)/3 − 4", 15, INK, "start")
    out += text(745, 252, "= 2.2 + 1.8 − 4 = 0 A  ✓", 15, GREEN, "middle", 700)
    out += text(525, 294, "ที่ B: (9−14.4)/3 + 9/5 + 4 − 4 = 0 A  ✓", 15, GREEN, "start", 700)

    out += rect(500, 365, 490, 405, SOFT, GRID)
    out += text(525, 402, "สมดุลกำลัง (บวก = ดูดกลืน, ลบ = จ่าย)", 17, GREEN, "start", 700)
    powers = [
        ("R₁", 9.68, "#0f766e"),
        ("R₂", 9.72, "#2563eb"),
        ("R₃", 16.20, "#7c3aed"),
        ("v_s", 22.00, "#b45309"),
    ]
    total = 57.6
    x0, bar_width, bar_y = 535, 420, 450
    cursor = x0
    for label, value, color in powers:
        segment = bar_width * value / total
        out += rect(cursor, bar_y, segment, 44, color, color, 0, 0)
        if segment > 62:
            out += text(cursor + segment / 2, bar_y + 28, f"{label} {value:g}", 12, PAPER,
                        "middle", 700)
        cursor += segment
    out += text(535, 522, "ดูดกลืนรวม 57.60 W", 14, MUTED, "start", 700)

    out += rect(x0, 550, bar_width * 21.6 / total, 44, CYAN, CYAN, 0, 0)
    out += rect(x0 + bar_width * 21.6 / total, 550, bar_width * 36 / total, 44,
                LINK, LINK, 0, 0)
    out += text(x0 + bar_width * 21.6 / total / 2, 578, "i_s บน 21.6", 12, PAPER,
                "middle", 700)
    out += text(x0 + bar_width * (21.6 + 18) / total, 578, "i_s ขวา 36.0", 12, PAPER,
                "middle", 700)
    out += text(535, 622, "แหล่งกระแสจ่ายรวม 57.60 W", 14, MUTED, "start", 700)

    out += rect(535, 660, 420, 75, "#ecfdf5", GREEN, 10, 1.7)
    out += math_text(745, 696, "Σp = 9.68+9.72+16.2+22−21.6−36", 17, INK)
    out += math_text(745, 722, "= 0 W  ✓", 19, GREEN, "middle", 700)
    out += tail()
    save("fig-08-numeric-power.svg", out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig01()
    fig02()
    fig03()
    fig04()
    fig05()
    fig06()
    fig07()
    fig08()
    print("done: generated 8 SVG figures")


if __name__ == "__main__":
    main()
