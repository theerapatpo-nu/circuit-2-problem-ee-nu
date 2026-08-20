#!/usr/bin/env python3
"""Generate the eight SVG teaching figures for circuit problem 4.5.

Run from any directory:
    python3 engineering-problem/circuit/2/chapter4/4.5/make_figures.py

Only the Python standard library is used.  SVG text stays as text so the
figures remain sharp, searchable, and accessible at every zoom level.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#172033"
MUTED = "#64748b"
GRID = "#cbd5e1"
PAPER = "#ffffff"
SOFT = "#f8fafc"
BLUE = "#2563eb"
RED = "#dc2626"
GREEN = "#059669"
PURPLE = "#7c3aed"
AMBER = "#b45309"
CYAN = "#0891b2"
PINK = "#db2777"
FONT = "'Noto Sans Thai','Sarabun','IBM Plex Sans Thai','Segoe UI',sans-serif"
MATH = "'STIX Two Math','Cambria Math','Times New Roman',serif"

MARKERS = {
    INK: "ink", BLUE: "blue", RED: "red", GREEN: "green",
    PURPLE: "purple", AMBER: "amber", CYAN: "cyan", PINK: "pink",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def svg_head(width: int, height: int, title: str) -> str:
    markers = []
    for color, name in MARKERS.items():
        markers.append(
            f'<marker id="arr-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{color}"/></marker>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{esc(title)}" font-family="{FONT}">\n'
        f'<title>{esc(title)}</title><defs>{"".join(markers)}</defs>\n'
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>\n'
    )


def text(x: float, y: float, value: object, size: float = 18,
         color: str = INK, anchor: str = "middle", weight: int = 400,
         family: str = FONT) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}" font-weight="{weight}" font-family="{family}">'
        f'{esc(value)}</text>\n'
    )


def lines(x: float, y: float, values: list[str], size: float = 17,
          color: str = INK, anchor: str = "start", gap: float = 28,
          weight: int = 400, family: str = FONT) -> str:
    return "".join(
        text(x, y + index * gap, value, size, color, anchor, weight, family)
        for index, value in enumerate(values)
    )


def math_text(x: float, y: float, value: object, size: float = 20,
              color: str = INK, anchor: str = "middle", weight: int = 400) -> str:
    return text(x, y, value, size, color, anchor, weight, MATH)


def rect(x: float, y: float, width: float, height: float, fill: str = PAPER,
         stroke: str = GRID, radius: float = 18, stroke_width: float = 1.5,
         dash: str | None = None) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{dashed}/>\n'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = INK,
         width: float = 2.6, dash: str | None = None) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dashed}/>\n'
    )


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = BLUE,
          width: float = 2.7, dash: str | None = None) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    marker = MARKERS[color]
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
        f'marker-end="url(#arr-{marker})"{dashed}/>\n'
    )


def path(d: str, color: str = INK, width: float = 2.6,
         fill: str = "none", arrow_end: bool = False,
         dash: str | None = None) -> str:
    marker = f' marker-end="url(#arr-{MARKERS[color]})"' if arrow_end else ""
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round"{marker}{dashed}/>\n'
    )


def circle(cx: float, cy: float, radius: float, fill: str = PAPER,
           stroke: str = INK, width: float = 2.4) -> str:
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{width}"/>\n'
    )


def node(x: float, y: float, label: str | None = None,
         dx: float = 0, dy: float = -18) -> str:
    out = circle(x, y, 7, INK, INK, 1)
    if label:
        out += math_text(x + dx, y + dy, label, 21, INK, "middle", 700)
    return out


def resistor_points(x1: float, y1: float, x2: float, y2: float,
                    amplitude: float = 11, turns: int = 7) -> str:
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    pts = [(x1, y1)]
    for k in range(1, turns * 2):
        step = length * k / (turns * 2)
        sign = 1 if k % 2 else -1
        pts.append((x1 + ux * step + px * amplitude * sign,
                    y1 + uy * step + py * amplitude * sign))
    pts.append((x2, y2))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def resistor(x1: float, y1: float, x2: float, y2: float, label: str,
             color: str = INK, label_x: float | None = None,
             label_y: float | None = None) -> str:
    out = (
        f'<polyline points="{resistor_points(x1, y1, x2, y2)}" fill="none" '
        f'stroke="{color}" stroke-width="2.8" stroke-linejoin="round"/>\n'
    )
    lx = (x1 + x2) / 2 if label_x is None else label_x
    ly = (y1 + y2) / 2 - 20 if label_y is None else label_y
    return out + math_text(lx, ly, label, 21, color, "middle", 700)


def current_source(cx: float, cy: float, orientation: str, label: str,
                   color: str = PURPLE) -> str:
    out = circle(cx, cy, 29, PAPER, color, 2.6)
    if orientation == "up":
        out += arrow(cx, cy + 14, cx, cy - 14, color, 2.4)
        out += math_text(cx - 42, cy + 6, label, 20, color, "end", 700)
    elif orientation == "left":
        out += arrow(cx + 15, cy, cx - 15, cy, color, 2.4)
        out += math_text(cx, cy - 42, label, 20, color, "middle", 700)
    return out


def pill(x: float, y: float, width: float, label: str, color: str) -> str:
    return (
        rect(x, y, width, 38, color, color, 19, 1)
        + text(x + width / 2, y + 25, label, 15, PAPER, "middle", 700)
    )


def title_block(title: str, subtitle: str, width: int) -> str:
    return (
        text(54, 55, title, 29, INK, "start", 800)
        + text(54, 86, subtitle, 16, MUTED, "start", 400)
        + line(54, 105, width - 54, 105, GRID, 1.5)
    )


def save(name: str, body: str, width: int, height: int, title: str) -> None:
    (OUT / name).write_text(svg_head(width, height, title) + body + "</svg>\n", encoding="utf-8")


def fig_01() -> None:
    width, height = 1200, 690
    body = title_block("แผนที่การแก้โจทย์ 4.5", "รูป → topology → matrix → คำตอบ → การตรวจอิสระ", width)
    cards = [
        (60, 155, "1", "อ่านรูป", ["ระบุ A, B, O", "กำหนดทิศกิ่ง", "ล็อกทิศ iₓ"], BLUE),
        (295, 155, "2", "สร้าง B", ["T={2,3}", "L={1}", "B=[1  1  −1]"], RED),
        (530, 155, "3", "ปิด feedback", ["i=Bᵀj", "iₓ=I₀+j₁", "CCCS=αiₓ"], PURPLE),
        (765, 155, "4", "คูณ matrix", ["BZBᵀ", "BZiₛᵦ", "ระบบ 2×2"], GREEN),
        (1000, 155, "5", "คืนคำตอบ", ["j₁, iₓ", "i₁…i₃, v₁…v₃", "Vₐ, Vᵦ"], AMBER),
    ]
    for x, y, n, heading, details, color in cards:
        body += rect(x, y, 175, 240, SOFT, GRID)
        body += circle(x + 35, y + 40, 20, color, color, 1)
        body += text(x + 35, y + 47, n, 17, PAPER, "middle", 800)
        body += text(x + 20, y + 88, heading, 20, INK, "start", 700)
        body += lines(x + 20, y + 127, details, 15, MUTED, "start", 29)
    for x in [247, 482, 717, 952]:
        body += arrow(x, 275, x + 33, 275, CYAN, 3)
    body += rect(120, 455, 960, 155, "#eff6ff", BLUE, 20, 1.7)
    body += pill(150, 482, 130, "CHECK 4 มุม", BLUE)
    body += lines(150, 552, ["KVL ทุกวงรอบ", "KCL ทุกปม"], 17, INK, "start", 32, 600)
    body += lines(445, 552, ["Limiting cases", "กรณี D=0"], 17, INK, "start", 32, 600)
    body += lines(745, 552, ["Tellegen / power", "ตัวอย่างตัวเลข"], 17, INK, "start", 32, 600)
    save("fig-01-roadmap.svg", body, width, height, "แผนที่การแก้โจทย์วงจร 4.5")


def fig_02() -> None:
    width, height = 1200, 790
    body = title_block("อ่านวงจรให้เห็นปมและทิศ", "วงจรจริงทางซ้าย — กิ่งประกอบที่ใช้สร้าง B ทางขวา", width)
    body += rect(45, 135, 720, 600, SOFT, GRID)
    body += text(70, 172, "(ก) วงจรระดับอุปกรณ์", 20, INK, "start", 700)
    A, B, O = (250, 250), (610, 250), (430, 650)
    body += line(A[0], A[1], 170, A[1], INK)
    body += line(170, A[1], 170, 340, INK)
    body += current_source(170, 410, "up", "I₀", BLUE)
    body += line(170, 439, 170, O[1], INK)
    body += line(170, O[1], O[0], O[1], INK)
    body += line(A[0], A[1], A[0], 330, INK)
    body += resistor(A[0], 330, A[0], 510, "R₁", INK, 292, 430)
    body += line(A[0], 510, A[0], O[1], INK)
    body += line(A[0], O[1], O[0], O[1], INK)
    body += arrow(285, 350, 285, 485, RED, 2.8)
    body += math_text(302, 420, "iₓ", 21, RED, "start", 700)
    body += line(A[0], A[1], 325, A[1], INK)
    body += resistor(325, A[1], 535, A[1], "R₂", INK, 430, 220)
    body += line(535, A[1], B[0], B[1], INK)
    body += line(A[0], A[1], A[0], 355, INK)
    body += line(B[0], B[1], B[0], 355, INK)
    body += line(A[0], 355, 355, 355, INK)
    body += current_source(430, 355, "left", "αiₓ", PURPLE)
    body += line(459, 355, B[0], 355, INK)
    body += line(B[0], B[1], B[0], 335, INK)
    body += resistor(B[0], 335, B[0], 520, "R₃", INK, 650, 430)
    body += line(B[0], 520, B[0], O[1], INK)
    body += line(O[0], O[1], B[0], O[1], INK)
    body += node(*A, "A", -16, -20) + node(*B, "B", 16, -20) + node(*O, "O", 0, 30)
    body += arrow(120, 515, 120, 335, BLUE, 2.3)
    body += math_text(100, 430, "I₀", 18, BLUE, "end", 700)
    body += arrow(525, 390, 345, 390, PURPLE, 2.3)
    body += math_text(435, 420, "αiₓ", 18, PURPLE, "middle", 700)

    body += rect(795, 135, 360, 600, PAPER, GRID)
    body += text(820, 172, "(ข) กราฟ 3 กิ่งประกอบ", 20, INK, "start", 700)
    a, b, o = (860, 300), (1080, 300), (970, 610)
    body += line(o[0], o[1], b[0], b[1], RED, 4)
    body += line(b[0], b[1], a[0], a[1], INK, 4)
    body += line(o[0], o[1], a[0], a[1], INK, 4)
    body += node(*a, "A", -10, -20) + node(*b, "B", 10, -20) + node(*o, "O", 0, 31)
    body += arrow(1010, 508, 1063, 360, RED, 2.8)
    body += arrow(1040, 272, 900, 272, BLUE, 2.8)
    body += arrow(935, 515, 883, 365, BLUE, 2.8)
    body += pill(1000, 425, 90, "กิ่ง 1", RED)
    body += pill(925, 238, 90, "กิ่ง 2", BLUE)
    body += pill(840, 425, 90, "กิ่ง 3", BLUE)
    body += lines(825, 685, ["1: O→B", "2: B→A", "3: O→A"], 16, MUTED, "start", 0)
    save("fig-02-circuit-anatomy.svg", body, width, height, "ปม อุปกรณ์ และกิ่งประกอบโจทย์ 4.5")


def fig_03() -> None:
    width, height = 1200, 700
    body = title_block("จาก tree อ่าน Tie-set Matrix", "เติม link 1 แล้วเดินตาม O→B→A→O", width)
    body += rect(55, 145, 470, 470, SOFT, GRID)
    body += text(85, 187, "Tree: T={2,3}", 21, INK, "start", 700)
    a, b, o = (145, 320), (430, 320), (285, 550)
    body += line(b[0], b[1], a[0], a[1], INK, 6)
    body += line(o[0], o[1], a[0], a[1], INK, 6)
    body += path(f"M {o[0]} {o[1]} L {b[0]} {b[1]}", RED, 5, "none", False, "10 9")
    body += node(*a, "A", -12, -20) + node(*b, "B", 12, -20) + node(*o, "O", 0, 30)
    body += pill(250, 290, 75, "2", INK) + pill(165, 425, 75, "3", INK)
    body += pill(365, 430, 75, "link 1", RED)
    body += path("M 304 520 C 395 500, 470 405, 432 340", RED, 3, "none", True)
    body += path("M 405 285 C 340 250, 220 250, 163 295", RED, 3, "none", True)
    body += path("M 135 345 C 130 410, 175 500, 265 538", RED, 3, "none", True)
    body += math_text(290, 238, "j₁", 22, RED, "middle", 700)

    body += rect(560, 145, 585, 470, PAPER, GRID)
    body += text(590, 187, "อ่านทีละคอลัมน์", 21, INK, "start", 700)
    rows = [
        (230, "กิ่ง 1", "ตามวงรอบ", "+1", RED),
        (315, "กิ่ง 2", "ตามวงรอบ", "+1", BLUE),
        (400, "กิ่ง 3", "สวนวงรอบ", "−1", PURPLE),
    ]
    for y, branch, relation, value, color in rows:
        body += rect(590, y, 520, 62, SOFT, GRID, 12)
        body += pill(610, y + 12, 90, branch, color)
        body += text(735, y + 39, relation, 17, INK, "start", 600)
        body += math_text(1060, y + 42, value, 25, color, "middle", 800)
    body += math_text(850, 535, "B = [ 1   1   −1 ]", 31, INK, "middle", 700)
    body += math_text(850, 580, "i = Bᵀj = [ j₁  j₁  −j₁ ]ᵀ", 22, BLUE, "middle", 600)
    save("fig-03-tree-tieset.svg", body, width, height, "การสร้างเมทริกซ์ tie-set ของโจทย์ 4.5")


def fig_04() -> None:
    width, height = 1200, 690
    body = title_block("ตัวแปรควบคุมคือวงป้อนกลับ", "กิ่ง 3 ให้ iₓ — จากนั้น iₓ ควบคุมแหล่งในกิ่ง 2", width)
    body += rect(60, 155, 315, 400, "#eff6ff", BLUE)
    body += text(90, 198, "กิ่ง 3: KCL ภายใน", 20, BLUE, "start", 700)
    body += arrow(205, 475, 205, 245, BLUE, 3)
    body += math_text(174, 360, "I₀", 22, BLUE, "end", 700)
    body += arrow(285, 245, 285, 475, RED, 3)
    body += math_text(315, 360, "iₓ", 22, RED, "start", 700)
    body += arrow(120, 475, 120, 265, GREEN, 3)
    body += math_text(93, 370, "i₃", 22, GREEN, "end", 700)
    body += math_text(217, 520, "i₃ = I₀ − iₓ", 23, INK, "middle", 700)

    body += arrow(395, 350, 485, 350, CYAN, 4)
    body += rect(500, 155, 270, 400, "#faf5ff", PURPLE)
    body += text(530, 198, "ใช้ topology", 20, PURPLE, "start", 700)
    body += math_text(635, 280, "i₃ = −j₁", 28, PURPLE, "middle", 700)
    body += line(545, 320, 725, 320, GRID, 1.5)
    body += math_text(635, 385, "iₓ = I₀ − i₃", 24, INK, "middle", 600)
    body += math_text(635, 445, "iₓ = I₀ + j₁", 30, PURPLE, "middle", 800)
    body += pill(558, 485, 155, "CONTROL EQ.", PURPLE)

    body += arrow(790, 350, 880, 350, CYAN, 4)
    body += rect(895, 155, 250, 400, "#fff7ed", AMBER)
    body += text(925, 198, "กิ่ง 2: CCCS", 20, AMBER, "start", 700)
    body += circle(1020, 310, 55, PAPER, AMBER, 3)
    body += arrow(1050, 310, 990, 310, AMBER, 3)
    body += math_text(1020, 395, "αiₓ", 30, AMBER, "middle", 800)
    body += math_text(1020, 465, "v₂=R₂(j₁−αiₓ)", 22, INK, "middle", 600)
    body += text(600, 625, "ระบบจะปิดได้เมื่อสมการวงรอบและสมการควบคุมอยู่ใน matrix เดียวกัน", 19, MUTED, "middle", 600)
    save("fig-04-control-feedback.svg", body, width, height, "ตัวแปรควบคุมและ CCCS ในโจทย์ 4.5")


def fig_05() -> None:
    width, height = 1200, 720
    body = title_block("ประกอบเวกเตอร์แรงดันกิ่ง", "คูณทีละแถว แล้วลบเวกเตอร์ตำแหน่งเดียวกัน", width)
    body += rect(55, 145, 335, 470, SOFT, GRID)
    body += pill(85, 175, 160, "ก้อนตัวต้านทาน", BLUE)
    body += math_text(222, 260, "Zᵦ iᵦ", 28, BLUE, "middle", 700)
    body += math_text(222, 318, "[ R₃j₁ ]", 23, INK)
    body += math_text(222, 355, "[ R₂j₁ ]", 23, INK)
    body += math_text(222, 392, "[ −R₁j₁ ]", 23, INK)
    body += lines(85, 475, ["แถว 1: R₃·j₁", "แถว 2: R₂·j₁", "แถว 3: R₁·(−j₁)"], 16, MUTED, "start", 31)

    body += math_text(425, 385, "−", 42, RED, "middle", 800)

    body += rect(455, 145, 335, 470, SOFT, GRID)
    body += pill(485, 175, 145, "ก้อนแหล่งจ่าย", PURPLE)
    body += math_text(622, 260, "Zᵦ iₛᵦ", 28, PURPLE, "middle", 700)
    body += math_text(622, 318, "[ 0 ]", 23, INK)
    body += math_text(622, 355, "[ αR₂iₓ ]", 23, INK)
    body += math_text(622, 392, "[ R₁I₀ ]", 23, INK)
    body += lines(485, 475, ["กิ่ง 1: ไม่มี source", "กิ่ง 2: CCCS αiₓ", "กิ่ง 3: source I₀"], 16, MUTED, "start", 31)

    body += math_text(825, 385, "=", 42, GREEN, "middle", 800)

    body += rect(855, 145, 290, 470, "#ecfdf5", GREEN)
    body += pill(885, 175, 120, "ผลลัพธ์ vᵦ", GREEN)
    body += math_text(1000, 270, "vᵦ", 28, GREEN, "middle", 700)
    body += math_text(1000, 330, "[ R₃j₁ ]", 21, INK)
    body += math_text(1000, 370, "[ R₂(j₁−αiₓ) ]", 21, INK)
    body += math_text(1000, 410, "[ −R₁(j₁+I₀) ]", 21, INK)
    body += lines(885, 500, ["= [v₁  v₂  v₃]ᵀ", "ตรงกับ scalar ทุกกิ่ง"], 16, MUTED, "start", 31, 600)
    body += math_text(600, 670, "vᵦ = Zᵦ iᵦ − Zᵦ iₛᵦ", 26, INK, "middle", 700)
    save("fig-05-branch-vector.svg", body, width, height, "การประกอบเวกเตอร์แรงดันกิ่งโจทย์ 4.5")


def fig_06() -> None:
    width, height = 1200, 830
    body = title_block("Matrix Engine: ทุกสัมประสิทธิ์มีที่มา", "สามก้อนจาก lecture แล้วปิดระบบด้วย control equation", width)
    body += rect(50, 135, 1100, 185, SOFT, GRID)
    blocks = [
        (75, "1  LOOP MATRIX", "BZᵦBᵀ", "= R₁+R₂+R₃ = Rₜ", BLUE),
        (405, "2  CCCS TERM", "BZᵦ[0 αiₓ 0]ᵀ", "= +αR₂iₓ", PURPLE),
        (760, "3  I₀ TERM", "BZᵦ[0 0 I₀]ᵀ", "= −R₁I₀", AMBER),
    ]
    for x, label, formula, result, color in blocks:
        body += pill(x, 158, 160, label, color)
        body += math_text(x + 145, 235, formula, 21, INK, "middle", 600)
        body += math_text(x + 145, 282, result, 21, color, "middle", 700)
    body += arrow(600, 335, 600, 390, CYAN, 4)
    body += rect(130, 405, 940, 285, "#eff6ff", BLUE, 22, 2)
    body += pill(165, 435, 185, "AUGMENTED SYSTEM", BLUE)
    body += math_text(600, 540, "[ Rₜ    −αR₂ ] [ j₁ ]   =   [ −R₁I₀ ]", 31, INK, "middle", 700)
    body += math_text(600, 594, "[ −1       1  ] [ iₓ ]       [   I₀    ]", 31, INK, "middle", 700)
    body += line(180, 625, 1020, 625, GRID, 1.5)
    body += math_text(600, 667, "det = D = Rₜ − αR₂", 25, RED, "middle", 800)
    body += rect(170, 730, 395, 58, "#ecfdf5", GREEN, 14, 1.5)
    body += math_text(367, 767, "j₁=(αR₂−R₁)I₀ / D", 22, GREEN, "middle", 700)
    body += rect(635, 730, 395, 58, "#faf5ff", PURPLE, 14, 1.5)
    body += math_text(832, 767, "iₓ=(R₂+R₃)I₀ / D", 22, PURPLE, "middle", 700)
    save("fig-06-matrix-engine.svg", body, width, height, "เครื่องยนต์เมทริกซ์ของโจทย์ 4.5")


def fig_07() -> None:
    width, height = 1200, 830
    body = title_block("แผนที่คำตอบเชิงสัญลักษณ์", "กำหนด D=R₁+R₃+(1−α)R₂ และ D≠0", width)
    body += rect(430, 135, 340, 110, "#fff7ed", AMBER, 18, 2)
    body += math_text(600, 180, "D = R₁+R₃+(1−α)R₂", 24, AMBER, "middle", 800)
    body += math_text(600, 220, "common denominator", 16, MUTED, "middle", 500)
    body += arrow(600, 250, 600, 300, CYAN, 3)

    cards = [
        (65, 320, 330, 160, "ตัวแปรหลัก", ["j₁=(αR₂−R₁)I₀/D", "iₓ=(R₂+R₃)I₀/D"], BLUE),
        (435, 320, 330, 160, "กระแสกิ่ง", ["i₁=i₂=j₁", "i₃=−j₁"], GREEN),
        (805, 320, 330, 160, "แรงดันปม", ["Vₐ=R₁(R₂+R₃)I₀/D", "Vᵦ=R₃(R₁−αR₂)I₀/D"], PURPLE),
        (65, 540, 330, 200, "แรงดันกิ่ง 1", ["v₁=R₃j₁", "=R₃(αR₂−R₁)I₀/D"], RED),
        (435, 540, 330, 200, "แรงดันกิ่ง 2", ["v₂=R₂(j₁−αiₓ)", "=−R₂(R₁+αR₃)I₀/D"], AMBER),
        (805, 540, 330, 200, "แรงดันกิ่ง 3", ["v₃=−R₁iₓ", "=−R₁(R₂+R₃)I₀/D"], CYAN),
    ]
    for x, y, w, h, heading, formulas, color in cards:
        body += rect(x, y, w, h, SOFT, color, 18, 1.7)
        body += pill(x + 22, y + 22, 145, heading, color)
        body += math_text(x + w / 2, y + 95, formulas[0], 19, INK, "middle", 600)
        body += math_text(x + w / 2, y + 132, formulas[1], 18, color, "middle", 700)
    body += text(600, 795, "ขั้วแรงดันกิ่ง: + ที่ต้นลูกศร และ − ที่ปลายลูกศร", 17, MUTED, "middle", 600)
    save("fig-07-answer-map.svg", body, width, height, "แผนที่คำตอบเชิงสัญลักษณ์โจทย์ 4.5")


def fig_08() -> None:
    width, height = 1200, 810
    body = title_block("ตรวจคำตอบด้วยตัวเลขและกำลัง", "R₁=2Ω, R₂=3Ω, R₃=5Ω, α=0.5, I₀=4A", width)
    body += rect(55, 140, 520, 280, SOFT, GRID)
    body += pill(85, 168, 145, "NUMERIC STATE", BLUE)
    numeric = [
        "D = 17/2 Ω",
        "j₁ = −4/17 A",
        "iₓ = 64/17 A",
        "Vₐ = 128/17 V",
        "Vᵦ = 20/17 V",
    ]
    body += lines(90, 240, numeric, 19, INK, "start", 34, 600, MATH)
    body += rect(625, 140, 520, 280, "#ecfdf5", GREEN)
    body += pill(655, 168, 140, "KVL + NODE", GREEN)
    body += math_text(885, 250, "v₁+v₂−v₃", 24, INK, "middle", 600)
    body += math_text(885, 295, "= (−20−108+128)/17", 20, MUTED, "middle", 500)
    body += math_text(885, 340, "= 0 V ✓", 28, GREEN, "middle", 800)
    body += math_text(885, 385, "Vᵦ−Vₐ = −108/17 V = v₂ ✓", 18, GREEN, "middle", 700)

    body += rect(55, 465, 1090, 280, PAPER, GRID)
    body += pill(85, 493, 155, "POWER BALANCE", PURPLE)
    powers = [
        ("R₁", 28.346, GREEN), ("R₂", 13.453, GREEN), ("R₃", 0.277, GREEN),
        ("I₀", -30.118, RED), ("CCCS", -11.958, RED),
    ]
    base_x, base_y, scale = 310, 620, 9.0
    body += line(base_x, 535, base_x, 705, INK, 2)
    body += line(250, base_y, 1080, base_y, INK, 2)
    x = 380
    for label, value, color in powers:
        height_bar = abs(value) * scale / 3
        if value >= 0:
            y = base_y - height_bar
        else:
            y = base_y
        body += rect(x, y, 90, height_bar, color, color, 7, 1)
        body += text(x + 45, base_y + 30, label, 16, INK, "middle", 700)
        label_y = y - 10 if value >= 0 else y + height_bar + 22
        body += text(x + 45, label_y, f"{value:+.3f}", 14, color, "middle", 700)
        x += 135
    body += text(180, 585, "ดูดกลืน +", 15, GREEN, "middle", 700)
    body += text(180, 670, "จ่าย −", 15, RED, "middle", 700)
    body += math_text(950, 525, "Σp = 0 W ✓", 24, PURPLE, "middle", 800)
    body += text(600, 785, "28.346 + 13.453 + 0.277 − 30.118 − 11.958 = 0.000 W", 18, INK, "middle", 700)
    save("fig-08-verification.svg", body, width, height, "การตรวจคำตอบและสมดุลกำลังโจทย์ 4.5")


def main() -> None:
    fig_01()
    fig_02()
    fig_03()
    fig_04()
    fig_05()
    fig_06()
    fig_07()
    fig_08()
    print(f"Generated 8 SVG files in {OUT}")


if __name__ == "__main__":
    main()
