#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างสื่อประกอบเฉลยโจทย์ [4.3] — Loop (Tie-set) Analysis
รันจากโฟลเดอร์ 4.3/ :  python3 assets/make_figures.py
ผลลัพธ์: assets/fig-XX-*.svg
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- palette ----------
INK    = "#16181d"   # เส้นวงจรหลัก
MUTED  = "#6b7280"   # เส้นช่วย/ตัวอักษรรอง
TWIG   = "#111827"   # กิ่งต้นไม้ (twig)  -> ดำหนา
LINK   = "#c0392b"   # กิ่งเชื่อม (link)  -> แดง
LOOP   = "#c0392b"   # กระแสวงรอบ
B1     = "#1d4ed8"   # สีประจำกิ่งที่ 1
B2     = "#047857"   # สีประจำกิ่งที่ 2
B1BG   = "#eff6ff"
B2BG   = "#ecfdf5"
SRC    = "#7c3aed"
WARN   = "#b45309"
PAPER  = "#ffffff"

FONT = "'Sarabun','Noto Sans Thai','IBM Plex Sans Thai',-apple-system,'Segoe UI',sans-serif"
MATH = "'Latin Modern Math','Cambria Math','Times New Roman',Georgia,serif"


def head(w, h, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"
     font-family="{FONT}" role="img" aria-label="{title}">
  <title>{title}</title>
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/>
    </marker>
    <marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/>
    </marker>
  </defs>
  <rect width="{w}" height="{h}" fill="{PAPER}"/>
'''


def tail():
    return "</svg>\n"


def _subs(s, size):
    """แปลง R_1 / v_{s} / x^2 ให้เป็น <tspan> ตัวห้อย-ตัวยก"""
    out, i, sz = [], 0, f"{size*0.68:.1f}"
    while i < len(s):
        c = s[i]
        if c in "_^" and i + 1 < len(s):
            i += 1
            if s[i] == "{":
                j = s.index("}", i)
                grp, i = s[i + 1:j], j + 1
            else:
                grp, i = s[i], i + 1
            shift = "sub" if c == "_" else "super"
            out.append(f'<tspan font-size="{sz}" baseline-shift="{shift}">{grp}</tspan>')
        else:
            out.append(c.replace("&", "&amp;").replace("<", "&lt;"))
            i += 1
    return "".join(out)


def txt(x, y, s, size=15, fill=INK, anchor="middle", weight="400", style="normal", family=None, extra=""):
    fam = family or FONT
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}" font-family="{fam}" {extra}>{_subs(s, size)}</text>\n')


def tri(x, y, w=20, h=22, color=INK, up=True):
    """หัวลูกศรสามเหลี่ยมขนาดคงที่ (ไม่ผูกกับ stroke-width)"""
    d = 1 if up else -1
    return (f'<polygon points="{x},{y + d*(-h/2)} {x - w/2},{y + d*(h/2)} {x + w/2},{y + d*(h/2)}" '
            f'fill="{color}"/>\n')


def mtxt(x, y, s, size=16, fill=INK, anchor="middle", weight="400"):
    """ข้อความคณิตศาสตร์ (ตัวเอียง serif)"""
    return txt(x, y, s, size, fill, anchor, weight, "italic", MATH)


def line(x1, y1, x2, y2, stroke=INK, w=2.6, dash=None, cap="round", extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{w}" stroke-linecap="{cap}"{d} {extra}/>\n')


def poly(pts, stroke=INK, w=2.6, fill="none", dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linejoin="round" stroke-linecap="round"{d} {extra}/>\n')


def zig(x1, y1, x2, y2, amp=11, n=6):
    """จุดของสัญลักษณ์ตัวต้านทานแบบฟันเลื่อย ระหว่าง (x1,y1)-(x2,y2)"""
    import math
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux                      # หน่วยตั้งฉาก
    step = L / (2 * n)
    pts = [(x1, y1)]
    s = step / 2
    for k in range(2 * n):
        sign = 1 if k % 2 == 0 else -1
        pts.append((x1 + ux * s + px * amp * sign, y1 + uy * s + py * amp * sign))
        s += step
    pts.append((x2, y2))
    return pts


def resistor(x1, y1, x2, y2, label=None, lx=0, ly=0, color=INK, w=2.6, size=17, lab_fill=None):
    s = poly(zig(x1, y1, x2, y2), stroke=color, w=w)
    if label:
        s += mtxt((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, size, lab_fill or color)
    return s


def node_dot(x, y, r=5.5, fill=INK):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>\n'


def vsource(cx, cy, r=23, color=INK, label=None, lx=-44, plus_top=True):
    """แหล่งกำเนิดแรงดัน วงกลม + / -"""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{color}" stroke-width="2.6"/>\n'
    yp, ym = (cy - 9, cy + 9) if plus_top else (cy + 9, cy - 9)
    s += line(cx - 7, yp, cx + 7, yp, color, 2.4)
    s += line(cx, yp - 7, cx, yp + 7, color, 2.4)
    s += line(cx - 7, ym, cx + 7, ym, color, 2.4)
    if label:
        s += mtxt(cx + lx, cy + 6, label, 17, color)
    return s


def isource(cx, cy, r=23, color=INK, label=None, lx=44, up=True):
    """แหล่งกำเนิดกระแส วงกลมมีลูกศร"""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{color}" stroke-width="2.6"/>\n'
    y1, y2 = (cy + 14, cy - 14) if up else (cy - 14, cy + 14)
    s += (f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="{color}" stroke-width="2.6" '
          f'marker-end="url(#ah)"/>\n')
    if label:
        s += mtxt(cx + lx, cy + 6, label, 17, color)
    return s


def arrow(x1, y1, x2, y2, color=INK, w=2.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" marker-end="url(#ah)"{d}/>\n')


def curve_arrow(d, color=INK, w=2.4, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'marker-end="url(#ah)"{da}/>\n')


def box(x, y, w, h, stroke=MUTED, fill="none", dash="7 5", r=10, sw=2):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-dasharray="{dash}"/>\n')


def panel(x, y, w, h, fill="#f8fafc", stroke="#e2e8f0", r=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n'


def save(name, body):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name)


# ---------- ตัวช่วยพิมพ์สัญลักษณ์คณิตศาสตร์ (รองรับ _ และ ^) ----------
def M(x, y, s, size=17, fill=INK, anchor="middle", weight="400", italic=True, family=None):
    """M(x,y,'R_1')  /  M(x,y,'v_{s}')  /  M(x,y,'j_1')  -> <text> พร้อม tspan ตัวห้อย/ตัวยก"""
    fam = family or MATH
    out, i, sub = [], 0, f'{size*0.66:.1f}'
    while i < len(s):
        c = s[i]
        if c in "_^" and i + 1 < len(s):
            i += 1
            if s[i] == "{":
                j = s.index("}", i)
                grp, i = s[i + 1:j], j + 1
            else:
                grp, i = s[i], i + 1
            shift = "sub" if c == "_" else "super"
            out.append(f'<tspan font-size="{sub}" baseline-shift="{shift}" font-style="normal">{grp}</tspan>')
        else:
            out.append(c.replace("&", "&amp;").replace("<", "&lt;"))
            i += 1
    st = "italic" if italic else "normal"
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{st}" font-family="{fam}">{"".join(out)}</text>\n')


def bullet(x, y, s, size=15, fill=INK, dot=True, dotc=None):
    out = ""
    if dot:
        out += f'<circle cx="{x-11}" cy="{y-5}" r="3.4" fill="{dotc or MUTED}"/>\n'
    out += txt(x, y, s, size, fill, "start")
    return out




def brackets(x1, x2, y1, y2, color=INK, w=2.2, ear=9):
    return (f'<path d="M {x1+ear} {y1} L {x1} {y1} L {x1} {y2} L {x1+ear} {y2}" fill="none" stroke="{color}" stroke-width="{w}"/>\n'
            f'<path d="M {x2-ear} {y1} L {x2} {y1} L {x2} {y2} L {x2-ear} {y2}" fill="none" stroke="{color}" stroke-width="{w}"/>\n')


def base_circuit(dx, dy, color=INK, lw=2.8):
    """วาดวงจรต้นฉบับ (ก): มุมซ้ายบนของราง = (dx,dy) ขนาด 570 x 220"""
    TOP, BOT = dy, dy + 220
    XL, XA, XR = dx, dx + 290, dx + 570
    s = ""
    s += line(XL, TOP, XL, dy + 87, color, lw)
    s += vsource(XL, dy + 110, 23, color)
    s += line(XL, dy + 133, XL, BOT, color, lw)
    s += line(XL, TOP, XL + 55, TOP, color, lw)
    s += poly(zig(XL + 55, TOP, XL + 215, TOP), color, lw)
    s += line(XL + 215, TOP, XA, TOP, color, lw)
    s += line(XA, TOP, XA, dy + 87, color, lw)
    s += isource(XA, dy + 110, 23, color)
    s += line(XA, dy + 133, XA, BOT, color, lw)
    s += line(XA, TOP, XA + 55, TOP, color, lw)
    s += poly(zig(XA + 55, TOP, XA + 215, TOP), color, lw)
    s += line(XA + 215, TOP, XR, TOP, color, lw)
    s += line(XR, TOP, XR, dy + 60, color, lw)
    s += poly(zig(XR, dy + 60, XR, dy + 165), color, lw)
    s += line(XR, dy + 165, XR, BOT, color, lw)
    s += line(XL, BOT, XR, BOT, color, lw)
    return s


def outer_loop(XL, XR, TOP, ybot, label, color=LOOP):
    """วงรอบ j1 (ทวนเข็มนาฬิกา) วาดอ้อมนอกวงจร: ขึ้นทางขวา ลงทางซ้าย"""
    xl, xr, yt = XL - 95, XR + 105, TOP - 52
    d = (f"M {xr} {ybot} L {xr} {yt+14} Q {xr} {yt} {xr-16} {yt} "
         f"L {xl+16} {yt} Q {xl} {yt} {xl} {yt+14} L {xl} {ybot}")
    s = curve_arrow(d, color, 2.4, "9 6")
    s += txt((xl + xr) / 2, yt - 10, label, 17, color, weight="700")
    return s


# =====================================================================
# รูปที่ 1 — กายวิภาคของรูป 4บ.3(ก)
# =====================================================================
def fig01():
    W, H = 900, 650
    dx, dy = 165, 150
    TOP, BOT = dy, dy + 220
    XL, XA, XR = dx, dx + 290, dx + 570
    s = head(W, H, "กายวิภาคของวงจรในรูป 4บ.3(ก)")
    s += txt(W / 2, 40, "รูปที่ 1 — อ่านรูป 4บ.3(ก) ทีละจุด: มีอะไรบ้าง ต่อกันอย่างไร", 20, INK, weight="700")
    s += txt(W / 2, 66, "องค์ประกอบ 5 ตัว • ปมทางเรขาคณิต 4 ปม • ปมที่ใช้จริงเพียง 2 ปม", 14.5, MUTED)
    s += base_circuit(dx, dy)

    s += M(XL + 148, TOP - 20, "R_1", 18, anchor="end")
    s += txt(XL + 156, TOP - 20, "[Ω]", 14, MUTED, "start")
    s += M(XA + 148, TOP - 20, "R_2", 18, anchor="end")
    s += txt(XA + 156, TOP - 20, "[Ω]", 14, MUTED, "start")
    s += M(XR + 26, dy + 112, "R_3", 18, anchor="start")
    s += txt(XR + 26, dy + 134, "[Ω]", 14, MUTED, "start")
    s += M(XL - 34, dy + 112, "v_s", 18, anchor="end")
    s += txt(XL - 34, dy + 134, "[V]", 14, MUTED, "end")
    s += M(XA + 34, dy + 112, "i_s", 18, anchor="start")
    s += txt(XA + 34, dy + 134, "[A]", 14, MUTED, "start")

    s += f'<circle cx="{XA}" cy="{TOP}" r="12" fill="none" stroke="{B1}" stroke-width="2.2"/>\n'
    s += node_dot(XA, TOP, 6, B1)
    s += M(XA + 20, TOP - 22, "a", 19, B1, "start", "700")
    s += txt(XA + 38, TOP - 22, "(ดีกรี 3)", 13, B1, "start")

    s += f'<circle cx="{XA}" cy="{BOT}" r="12" fill="none" stroke="{B2}" stroke-width="2.2"/>\n'
    s += node_dot(XA, BOT, 6, B2)
    s += line(XA, BOT, XA, BOT + 14, B2, 2.4)
    s += line(XA - 15, BOT + 14, XA + 15, BOT + 14, B2, 3)
    s += line(XA - 9, BOT + 20, XA + 9, BOT + 20, B2, 3)
    s += line(XA - 4, BOT + 26, XA + 4, BOT + 26, B2, 3)
    s += M(XA - 24, BOT + 24, "o", 19, B2, "end", "700")
    s += txt(XA + 30, BOT + 24, "= ปมอ้างอิง (datum) ดีกรี 3", 13, B2, "start")

    for X, nm, tx, anc in ((XL, "c", XL + 34, "start"), (XR, "d", XR - 34, "end")):
        s += node_dot(X, TOP, 5, WARN)
        s += f'<circle cx="{X}" cy="{TOP}" r="11" fill="none" stroke="{WARN}" stroke-width="1.8" stroke-dasharray="3 3"/>\n'
        s += M(X + (14 if anc == "start" else -14), TOP + 26, nm, 17, WARN, "middle", "700")
        s += txt(tx, TOP - 54, "ปมดีกรี 2 → ยุบได้", 13, WARN, anc)
    s += curve_arrow(f"M {XL+30} {TOP-50} Q {XL+4} {TOP-40} {XL-2} {TOP-16}", WARN, 1.8, "5 4")
    s += curve_arrow(f"M {XR-30} {TOP-50} Q {XR-4} {TOP-40} {XR+1} {TOP-16}", WARN, 1.8, "5 4")

    s += panel(60, 440, 780, 178)
    s += txt(84, 470, "สิ่งที่อ่านได้จากรูป (ก)", 16, INK, "start", "700")
    s += bullet(96, 500, "ทางเดินซ้าย: v_s ต่ออนุกรมกับ R₁ เชื่อมจากราง o ขึ้นไปยังปม a  (ขั้ว + ของ v_s อยู่ด้านบน)", 14.5, INK, dotc=B2)
    s += bullet(96, 526, "ทางเดินกลาง: i_s ชี้ขึ้น อัดกระแสจากราง o เข้าสู่ปม a", 14.5, INK, dotc=B1)
    s += bullet(96, 552, "ทางเดินขวา: R₂ ต่ออนุกรม R₃ จากปม a ลงกลับสู่ราง o  (ปม d เป็นเพียงจุดต่ออนุกรม)", 14.5, INK, dotc=B1)
    s += bullet(96, 578, "จึงเหลือปมที่มีความหมายเพียง 2 ปม คือ a และ o — องค์ประกอบทั้งหมดขนานกันคร่อม a–o", 14.5, INK, dotc=MUTED)
    s += tail()
    save("fig-01-figure-a-anatomy.svg", s)


# =====================================================================
# รูปที่ 2 — จัดกลุ่มองค์ประกอบเป็น "กิ่งประกอบ" 2 กิ่ง
# =====================================================================
def fig02():
    W, H = 900, 800
    dx, dy = 165, 120
    TOP, BOT = dy, dy + 220
    XL, XA, XR = dx, dx + 290, dx + 570
    s = head(W, H, "การยุบวงจรเป็นกิ่งประกอบ 2 กิ่ง")
    s += txt(W / 2, 38, "รูปที่ 2 — จับกลุ่มองค์ประกอบตามที่โจทย์กำหนด ให้เหลือกิ่งประกอบ 2 กิ่ง", 20, INK, weight="700")

    s += box(XL - 48, TOP - 34, 286, 190, B2, B2BG, "8 5", 14, 2.4)
    s += box(XA - 48, TOP - 34, 366, 226, B1, B1BG, "8 5", 14, 2.4)
    s += base_circuit(dx, dy)
    s += M(XL + 135, TOP - 50, "R_1", 17)
    s += M(XA + 135, TOP - 50, "R_2", 17)
    s += M(XR - 28, dy + 116, "R_3", 17, anchor="end")
    s += M(XL - 36, dy + 116, "v_s", 17, anchor="end")
    s += M(XA + 32, dy + 116, "i_s", 17, anchor="start")
    s += node_dot(XA, TOP, 6, INK)
    s += node_dot(XA, BOT, 6, INK)
    s += M(XA - 16, TOP - 12, "a", 17, INK, "end", "700")
    s += M(XA - 16, BOT + 22, "o", 17, INK, "end", "700")

    s += txt(XL - 40, TOP - 46, "กิ่งที่ 2", 16, B2, "start", "700")
    s += txt(XL - 48, BOT + 34, "v_s อนุกรมกับ R₁  (รูปทีวินิน)", 13.5, B2, "start")
    s += txt(XR + 44, TOP - 46, "กิ่งที่ 1", 16, B1, "end", "700")
    s += txt(XR + 44, BOT + 34, "i_s ขนานกับ (R₂ อนุกรม R₃)  (รูปนอร์ตัน)", 13.5, B1, "end")

    s += arrow(W / 2, 396, W / 2, 436, MUTED, 2.4)
    s += txt(W / 2 + 16, 424, "ยุบเป็นกราฟ 2 ปม 2 กิ่ง", 14.5, MUTED, "start")

    yA, yO = 516, 666
    s += line(255, yA, 675, yA, INK, 3)
    s += line(255, yO, 675, yO, INK, 3)
    s += M(240, yA - 12, "a", 18, INK, "end", "700")
    s += M(240, yO + 26, "o", 18, INK, "end", "700")
    for X, col, bg, name, inner, ivar, vvar in (
            (570, B1, B1BG, "กิ่งที่ 1", "i_s ขนาน (R₂+R₃)", "i_1", "v_1"),
            (330, B2, B2BG, "กิ่งที่ 2", "v_s อนุกรม R₁", "i_2", "v_2")):
        s += line(X, yA, X, yA + 32, INK, 2.8)
        s += line(X, yO - 32, X, yO, INK, 2.8)
        s += f'<rect x="{X-62}" y="{yA+32}" width="124" height="{yO-32-(yA+32)}" rx="10" fill="{bg}" stroke="{col}" stroke-width="2.6"/>\n'
        s += txt(X, yA + 62, name, 15, col, weight="700")
        s += txt(X, yA + 86, inner, 14, col)
        s += node_dot(X, yA, 6, INK)
        s += node_dot(X, yO, 6, INK)
        s += arrow(X - 88, yO - 12, X - 88, yA + 12, col, 2.4)
        s += M(X - 100, (yA + yO) / 2 + 6, ivar, 17, col, "end")
        s += txt(X + 78, yO - 22, "+", 20, col, weight="700")
        s += txt(X + 78, yA + 30, "–", 20, col, weight="700")
        s += M(X + 96, (yA + yO) / 2 + 6, vvar, 17, col, "start")

    s += txt(W / 2, 726, "ทิศอ้างอิงของทั้งสองกิ่งชี้จาก o ขึ้นสู่ a  •  ใช้ขั้วแบบสัมพันธ์ (+ อยู่ที่หางลูกศร)", 14, MUTED)
    s += txt(W / 2, 752, "จึงได้ว่า  v₁ = v₂ = v(o) − v(a) = −v(a)   ซึ่งจะกลายเป็นสมการวงรอบในขั้นถัดไป", 14, MUTED)
    s += tail()
    save("fig-02-composite-branches.svg", s)


# =====================================================================
# รูปที่ 3 — กายวิภาคของรูป 4บ.3(ข)
# =====================================================================
def graph_tree(cx, cy, r=105, bend=150, loop_r=44, loop_dx=8, big=True):
    T, Bm = (cx, cy - r), (cx, cy + r)
    s = f'<path d="M {Bm[0]} {Bm[1]} Q {cx-bend} {cy} {T[0]} {T[1]}" fill="none" stroke="{TWIG}" stroke-width="7" stroke-linecap="round"/>\n'
    s += tri(cx - bend * 0.5, cy, 19, 21, TWIG, up=True)
    s += f'<path d="M {Bm[0]} {Bm[1]} Q {cx+bend} {cy} {T[0]} {T[1]}" fill="none" stroke="{LINK}" stroke-width="3.2" stroke-linecap="round"/>\n'
    s += tri(cx + bend * 0.5, cy, 15, 17, LINK, up=True)
    s += node_dot(*T, 9, INK)
    s += node_dot(*Bm, 9, INK)
    s += M(T[0] + 18, T[1] - 14, "a", 18, INK, "start", "700")
    s += M(Bm[0] + 18, Bm[1] + 28, "o", 18, INK, "start", "700")
    s += txt(cx - bend * 0.72, cy + 6, "2", 22, TWIG, "end", "700")
    s += txt(cx + bend * 0.72, cy + 6, "1", 22, LINK, "start", "700")
    lx = cx + loop_dx
    s += f'<circle cx="{lx}" cy="{cy}" r="{loop_r}" fill="none" stroke="{LOOP}" stroke-width="2.4" stroke-dasharray="7 6"/>\n'
    s += tri(lx - loop_r, cy, 13, 15, LOOP, up=False)
    s += M(lx + 14, cy + 7, "j_1", 20, LOOP, "start", "700")
    return s


def fig03():
    W, H = 900, 620
    cx, cy = 265, 290
    s = head(W, H, "กายวิภาคของทรีในรูป 4บ.3(ข)")
    s += txt(W / 2, 38, "รูปที่ 3 — อ่านรูป 4บ.3(ข): กราฟ ทรี ลิงก์ และทิศของกระแสวงรอบ", 20, INK, weight="700")
    s += graph_tree(cx, cy)

    x0 = 545
    s += panel(x0 - 25, 90, 330, 206, "#f8fafc")
    s += txt(x0 - 5, 120, "สิ่งที่รูป (ข) บอกเรา", 16, INK, "start", "700")
    s += f'<line x1="{x0-5}" y1="146" x2="{x0+28}" y2="146" stroke="{TWIG}" stroke-width="7" stroke-linecap="round"/>\n'
    s += txt(x0 + 40, 151, "เส้นทึบหนา = ทวิก (twig) คือกิ่งที่ 2", 13.5, INK, "start")
    s += f'<line x1="{x0-5}" y1="178" x2="{x0+28}" y2="178" stroke="{LINK}" stroke-width="3.2" stroke-linecap="round"/>\n'
    s += txt(x0 + 40, 183, "เส้นแดงบาง = ลิงก์ (link) คือกิ่งที่ 1", 13.5, INK, "start")
    s += f'<circle cx="{x0+11}" cy="210" r="12" fill="none" stroke="{LOOP}" stroke-width="2" stroke-dasharray="5 4"/>\n'
    s += txt(x0 + 40, 215, "วงกลมประ = กระแสวงรอบ j₁", 13.5, INK, "start")
    s += txt(x0 - 5, 248, "ลูกศรบนวงประอยู่ด้านซ้ายและชี้ลง ⇒ j₁ หมุน", 13, MUTED, "start")
    s += txt(x0 - 5, 270, "ทวนเข็มนาฬิกา ⇒ ตรงกับทิศของลิงก์ 1 พอดี", 13, MUTED, "start")

    rows = [("จำนวนปม  n", "2"), ("จำนวนกิ่ง  b", "2"),
            ("ทวิก  n − 1", "1  (กิ่งที่ 2)"), ("ลิงก์  b − n + 1", "1  (กิ่งที่ 1)"),
            ("จำนวนสมการวงรอบ", "1  ⇒ ตัวแปรเดียวคือ j₁")]
    ty = 320
    s += panel(x0 - 25, ty, 330, 30 + 30 * len(rows), "#ffffff", "#e2e8f0")
    s += txt(x0 - 5, ty + 24, "การนับทางโทโปโลยี", 15, INK, "start", "700")
    for k, (a, b) in enumerate(rows):
        yy = ty + 52 + 29 * k
        s += txt(x0 - 5, yy, a, 13.5, MUTED, "start")
        s += txt(x0 + 290, yy, b, 13.5, INK, "end", "600")

    s += panel(55, 470, 420, 110, "#fff7ed", "#fed7aa")
    s += txt(78, 500, "กฎที่ใช้ตลอดบทนี้", 15, WARN, "start", "700")
    s += txt(78, 526, "① ทิศของกระแสวงรอบ j₁ ยึดตามทิศของลิงก์เสมอ", 13.5, INK, "start")
    s += txt(78, 550, "② วงรอบพื้นฐานของลิงก์ 1 = ลิงก์ 1 + เส้นทางในทรี (กิ่ง 2)", 13.5, INK, "start")
    s += tail()
    save("fig-03-figure-b-anatomy.svg", s)


# =====================================================================
# รูปที่ 4 — แบบจำลองและสมการเฉพาะกิ่ง
# =====================================================================
def fig04():
    W, H = 940, 780
    s = head(W, H, "แบบจำลองและสมการเฉพาะกิ่ง")
    s += txt(W / 2, 38, "รูปที่ 4 — สมการเฉพาะกิ่ง: เขียน v ของแต่ละกิ่งในรูปของ i ของกิ่งนั้น", 20, INK, weight="700")
    s += txt(W / 2, 64, "ทิศอ้างอิงของทั้งสองกิ่งคือ o → a  และวางขั้ว + ไว้ที่หางลูกศร (ปม o)", 14.5, MUTED)

    s += panel(40, 100, 420, 470, B2BG, B2)
    s += panel(480, 100, 420, 470, B1BG, B1)
    s += txt(250, 132, "กิ่งที่ 2 — รูปทีวินิน (v_s อนุกรม R₁)", 16, B2, weight="700")
    s += txt(690, 132, "กิ่งที่ 1 — รูปนอร์ตัน (i_s ขนาน R₂+R₃)", 16, B1, weight="700")

    cx = 250
    s += line(cx, 500, cx, 454)
    s += vsource(cx, 430, 24)
    s += M(cx - 44, 436, "v_s", 17)
    s += line(cx, 406, cx, 340)
    s += poly(zig(cx, 340, cx, 260))
    s += M(cx - 44, 304, "R_1", 17)
    s += line(cx, 260, cx, 190)
    s += node_dot(cx, 190, 7)
    s += node_dot(cx, 500, 7)
    s += M(cx + 4, 176, "a", 18, INK, "start", "700")
    s += M(cx + 4, 524, "o", 18, INK, "start", "700")
    s += arrow(175, 480, 175, 212, B2, 2.6)
    s += M(158, 350, "i_2", 18, B2, "end")
    s += txt(cx + 52, 482, "+", 21, B2, weight="700")
    s += txt(cx + 52, 216, "–", 21, B2, weight="700")
    s += M(cx + 74, 350, "v_2", 18, B2, "start")
    s += txt(250, 548, "กระแส i₂ ไหลผ่านทั้ง v_s และ R₁ (อนุกรมกัน)", 13.5, MUTED)

    xs, xr = 620, 780
    s += line(xs, 190, xr, 190)
    s += line(xs, 500, xr, 500)
    s += line(xs, 500, xs, 399)
    s += isource(xs, 375, 24)
    s += M(xs - 42, 381, "i_s", 17)
    s += line(xs, 351, xs, 190)
    s += line(xr, 500, xr, 460)
    s += poly(zig(xr, 460, xr, 390))
    s += M(xr + 32, 428, "R_3", 17, anchor="start")
    s += line(xr, 390, xr, 350)
    s += poly(zig(xr, 350, xr, 280))
    s += M(xr + 32, 318, "R_2", 17, anchor="start")
    s += line(xr, 280, xr, 190)
    s += node_dot(690, 190, 7)
    s += node_dot(690, 500, 7)
    s += M(690, 176, "a", 18, INK, "middle", "700")
    s += M(690, 526, "o", 18, INK, "middle", "700")
    s += arrow(545, 480, 545, 212, B1, 2.6)
    s += M(528, 350, "i_1", 18, B1, "end")
    s += txt(866, 482, "+", 21, B1, weight="700")
    s += txt(866, 216, "–", 21, B1, weight="700")
    s += M(882, 350, "v_1", 18, B1, "start")
    s += arrow(xr - 34, 476, xr - 34, 424, WARN, 2.2)
    s += M(xr - 42, 458, "i_R", 15, WARN, "end")
    s += txt(690, 548, "กระแส i₁ แตกเป็น i_s กับ i_R ที่ผ่าน R₂ และ R₃", 13.5, MUTED)

    s += panel(40, 598, 420, 162, "#ffffff", B2)
    s += txt(64, 628, "เดินจาก o ขึ้นไป a ตามกิ่งที่ 2", 14.5, B2, "start", "700")
    s += txt(64, 656, "ผ่านแหล่งจ่ายจาก – ไป + ได้ +v_s  แล้วตกคร่อม R₁ เท่ากับ R₁i₂", 13, MUTED, "start")
    s += M(250, 690, "v(a) - v(o) = v_s - R_1 i_2", 18, INK)
    s += f'<rect x="60" y="708" width="382" height="40" rx="8" fill="{B2BG}" stroke="{B2}" stroke-width="1.6"/>\n'
    s += M(250, 735, "v_2 = v(o) - v(a) = R_1 i_2 - v_s", 18, B2, "middle", "600")

    s += panel(480, 598, 420, 162, "#ffffff", B1)
    s += txt(504, 628, "กระแสในกิ่งที่ 1 แยกเป็นสองทาง", 14.5, B1, "start", "700")
    s += txt(504, 656, "ส่วนที่ผ่าน R₂+R₃ คือ i_R = i₁ − i_s  ตกคร่อมเท่ากับ (R₂+R₃)i_R", 13, MUTED, "start")
    s += M(690, 690, "v(o) - v(a) = (R_2 + R_3)(i_1 - i_s)", 18, INK)
    s += f'<rect x="500" y="708" width="382" height="40" rx="8" fill="{B1BG}" stroke="{B1}" stroke-width="1.6"/>\n'
    s += M(690, 735, "v_1 = (R_2 + R_3)(i_1 - i_s)", 18, B1, "middle", "600")
    s += tail()
    save("fig-04-branch-models.svg", s)


# =====================================================================
# รูปที่ 5 — เมทริกซ์ tie-set
# =====================================================================
def fig05():
    W, H = 940, 640
    s = head(W, H, "เมทริกซ์ tie-set และการแปลงตัวแปร")
    s += txt(W / 2, 38, "รูปที่ 5 — เมทริกซ์วงรอบพื้นฐาน B และการแปลงตัวแปรทั้งสองทิศทาง", 20, INK, weight="700")

    s += panel(40, 78, 430, 236, "#ffffff", "#e2e8f0")
    s += txt(62, 108, "① กฎเครื่องหมายของ b_{1k}", 16, INK, "start", "700")
    s += f'<rect x="52" y="122" width="406" height="34" rx="7" fill="#eef2ff"/>\n'
    for t, x, a in (("กิ่ง k", 62, "start"), ("ทิศเทียบกับ j₁", 200, "start"), ("b_{1k}", 440, "end")):
        s += txt(x, 145, t, 14, "#3730a3", a, "700")
    for k, (a, b, c, col) in enumerate([("1  (ลิงก์)", "ทางเดียวกัน", "+1", LINK),
                                        ("2  (ทวิก)", "สวนทาง", "−1", TWIG)]):
        yy = 156 + 40 * k
        s += f'<rect x="52" y="{yy}" width="406" height="40" fill="{"#fafafa" if k%2 else "#ffffff"}"/>\n'
        s += txt(62, yy + 26, a, 14.5, col, "start", "600")
        s += txt(200, yy + 26, b, 14.5, INK, "start")
        s += txt(440, yy + 26, c, 16, col, "end", "700")
    s += txt(62, 268, "กิ่งที่ไม่อยู่ในวงรอบจะได้ 0 (โจทย์นี้ไม่มี)", 13.5, MUTED, "start")
    s += txt(62, 292, "ทุกกิ่งอยู่ในวงรอบเดียวกันหมด เพราะมีเพียง 2 กิ่ง", 13.5, MUTED, "start")

    s += panel(500, 78, 400, 236, "#ffffff", "#e2e8f0")
    s += txt(522, 108, "② เมทริกซ์วงรอบพื้นฐาน (1 × 2)", 16, INK, "start", "700")
    s += txt(672, 152, "กิ่ง 1", 13.5, LINK, weight="600")
    s += txt(762, 152, "กิ่ง 2", 13.5, TWIG, weight="600")
    s += M(608, 194, "B =", 20, INK, "end")
    s += brackets(622, 812, 168, 216)
    s += txt(672, 201, "+1", 20, LINK, weight="700")
    s += txt(762, 201, "−1", 20, TWIG, weight="700")
    s += txt(522, 252, "มีแถวเดียว เพราะมีลิงก์เดียว ⇒ วงรอบอิสระ 1 วง", 13.5, MUTED, "start")
    s += txt(522, 276, "เรียงหลักตามเลขกิ่ง 1, 2", 13.5, MUTED, "start")

    s += panel(40, 336, 430, 262, B1BG, B1)
    s += txt(62, 366, "③ กระแสกิ่งจากกระแสวงรอบ", 16, B1, "start", "700")
    s += M(150, 404, "i_b = B^{⊤} j", 20, INK)
    s += brackets(120, 200, 430, 502)
    s += M(160, 462, "i_1", 18, INK)
    s += M(160, 494, "i_2", 18, INK)
    s += M(226, 470, "=", 20, INK)
    s += brackets(252, 322, 430, 502)
    s += txt(287, 462, "+1", 18, LINK, weight="700")
    s += txt(287, 494, "−1", 18, TWIG, weight="700")
    s += M(352, 470, "j_1", 20, LOOP, "middle", "700")
    s += f'<rect x="60" y="524" width="390" height="58" rx="9" fill="#ffffff" stroke="{B1}" stroke-width="1.6"/>\n'
    s += M(140, 550, "i_1 = + j_1", 18, LINK, "middle", "600")
    s += M(330, 550, "i_2 = - j_1", 18, TWIG, "middle", "600")
    s += txt(255, 572, "กระแสทุกกิ่งขึ้นกับตัวแปรเดียว", 12.5, MUTED)

    s += panel(500, 336, 400, 262, B2BG, B2)
    s += txt(522, 366, "④ สมการวงรอบ (KVL)", 16, B2, "start", "700")
    s += M(700, 404, "B v_b = 0", 20, INK)
    s += brackets(556, 700, 446, 494)
    s += txt(596, 478, "+1", 18, LINK, weight="700")
    s += txt(664, 478, "−1", 18, TWIG, weight="700")
    s += brackets(714, 784, 430, 502)
    s += M(749, 462, "v_1", 18, INK)
    s += M(749, 494, "v_2", 18, INK)
    s += txt(800, 478, "= 0", 20, INK, "start")
    s += f'<rect x="520" y="524" width="360" height="58" rx="9" fill="#ffffff" stroke="{B2}" stroke-width="1.6"/>\n'
    s += M(700, 552, "v_1 - v_2 = 0", 19, B2, "middle", "600")
    s += txt(700, 574, "แรงดันสองกิ่งเท่ากันเสมอ", 12.5, MUTED)
    s += tail()
    save("fig-05-tieset-matrix.svg", s)


# =====================================================================
# รูปที่ 6 — เดินรอบวงรอบ แล้วแก้สมการ
# =====================================================================
def fig06():
    W, H = 940, 740
    s = head(W, H, "การเดินรอบวงรอบและการแก้สมการ")
    s += txt(W / 2, 38, "รูปที่ 6 — เดินรอบวงรอบเก็บเครื่องหมาย แล้วแก้หา j₁", 20, INK, weight="700")

    cx, cy = 235, 265
    s += graph_tree(cx, cy, r=95, bend=135, loop_r=40, loop_dx=6)
    s += f'<circle cx="{cx+104}" cy="{cy-62}" r="14" fill="{LINK}"/>\n'
    s += txt(cx + 104, cy - 57, "1", 15, "#fff", weight="700")
    s += f'<circle cx="{cx-104}" cy="{cy+62}" r="14" fill="{TWIG}"/>\n'
    s += txt(cx - 104, cy + 67, "2", 15, "#fff", weight="700")

    s += f'<circle cx="{68}" cy="{412}" r="12" fill="{LINK}"/>\n'
    s += txt(68, 417, "1", 13, "#fff", weight="700")
    s += txt(90, 417, "o → a  ตามลูกศรกิ่ง 1 (ตามทิศ j₁)  ⇒  +v₁", 14, LINK, "start", "600")
    s += f'<circle cx="{68}" cy="{442}" r="12" fill="{TWIG}"/>\n'
    s += txt(68, 447, "2", 13, "#fff", weight="700")
    s += txt(90, 447, "a → o  สวนลูกศรกิ่ง 2 (ตามทิศ j₁)  ⇒  −v₂", 14, TWIG, "start", "600")

    s += panel(40, 466, 400, 100, "#f8fafc")
    s += txt(62, 494, "ผลรวมแรงดันรอบวงรอบต้องเป็นศูนย์", 14.5, INK, "start", "700")
    s += M(240, 538, "(+1)v_1 + (-1)v_2 = 0", 19, INK)

    x0 = 480
    steps = [("แทนสมการเฉพาะกิ่งของแต่ละกิ่ง", "(R_2+R_3)(i_1 - i_s) - (R_1 i_2 - v_s) = 0"),
             ("แทนการแปลงกระแส  i₁ = j₁ ,  i₂ = −j₁", "(R_2+R_3)(j_1 - i_s) + R_1 j_1 + v_s = 0"),
             ("รวมพจน์ที่มี j₁ ไว้ข้างเดียวกัน", "(R_1+R_2+R_3) j_1 = (R_2+R_3)i_s - v_s")]
    s += txt(x0 - 16, 86, "แก้สมการทีละบรรทัด", 16, INK, "start", "700")
    for k, (cap, eq) in enumerate(steps):
        yy = 104 + 106 * k
        s += panel(x0 - 16, yy, 436, 84, "#ffffff", "#e2e8f0")
        s += f'<circle cx="{x0+6}" cy="{yy+26}" r="13" fill="#eef2ff"/>\n'
        s += txt(x0 + 6, yy + 31, str(k + 1), 14, "#3730a3", weight="700")
        s += txt(x0 + 28, yy + 31, cap, 13.5, MUTED, "start")
        s += M(x0 + 202, yy + 66, eq, 17, INK)
        if k < 2:
            s += arrow(x0 + 202, yy + 84, x0 + 202, yy + 102, MUTED, 1.8)

    s += f'<rect x="464" y="440" width="436" height="80" rx="12" fill="#fff7ed" stroke="{WARN}" stroke-width="2.4"/>\n'
    s += txt(682, 468, "คำตอบของกระแสวงรอบ", 14, WARN, weight="700")
    s += M(682, 500, "j_1 = [ (R_2+R_3)i_s - v_s ] / (R_1+R_2+R_3)", 17, INK, weight="600")

    s += panel(40, 586, 860, 130, "#f8fafc")
    s += txt(64, 616, "อ่านผลลัพธ์เดียวกันนี้ในรูปเมทริกซ์", 15, INK, "start", "700")
    s += M(64, 652, "R_{loop} = B R_b B^{⊤} = R_1 + R_2 + R_3", 17, INK, "start")
    s += M(64, 690, "R_{loop} j = B R_b i_{sb} + B v_{sb} = (R_2+R_3)i_s - v_s", 17, INK, "start")
    s += txt(560, 652, "ความต้านทานวงรอบ = ผลรวมความต้านทานรอบวง", 13, MUTED, "start")
    s += txt(560, 690, "ฝั่งขวา = แรงดันขับรวมรอบวง", 13, MUTED, "start")
    s += tail()
    save("fig-06-kvl-walk-and-solve.svg", s)


# =====================================================================
# รูปที่ 7 — คำตอบกำกับบนวงจร
# =====================================================================
def fig07():
    W, H = 940, 740
    dx, dy = 195, 150
    TOP, BOT = dy, dy + 220
    XL, XA, XR = dx, dx + 290, dx + 570
    s = head(W, H, "คำตอบแรงดันกิ่งและกระแสกิ่ง")
    s += txt(W / 2, 36, "รูปที่ 7 — ทิศทางจริงของกระแส และคำตอบเชิงสัญลักษณ์", 20, INK, weight="700")
    s += txt(W / 2, 60, "ให้  R_T = R₁ + R₂ + R₃   และสมมติว่า  v_s + R₁i_s > 0", 14, MUTED)

    s += outer_loop(XL, XR, TOP, dy + 150, "j_1  (ทวนเข็มนาฬิกา)")
    s += base_circuit(dx, dy)
    s += M(XL + 135, TOP - 18, "R_1", 17)
    s += M(XA + 135, TOP - 18, "R_2", 17)
    s += M(XR + 28, dy + 116, "R_3", 17, anchor="start")
    s += M(XL - 34, dy + 116, "v_s", 17, anchor="end")
    s += M(XA + 30, dy + 116, "i_s", 17, anchor="start")
    s += node_dot(XA, TOP, 6, INK)
    s += node_dot(XA, BOT, 6, INK)
    s += M(XA - 14, TOP - 12, "a", 17, INK, "end", "700")
    s += M(XA - 14, BOT + 24, "o", 17, INK, "end", "700")

    s += arrow(XL + 30, dy + 55, XL + 30, dy + 175, B2, 2.4)
    s += txt(XL + 42, dy + 108, "กระแสจริงไหลลง", 12.5, B2, "start")
    s += txt(XL + 42, dy + 128, "(กิ่งที่ 2)", 12.5, B2, "start")
    s += arrow(XR - 30, dy + 55, XR - 30, dy + 175, B1, 2.4)
    s += txt(XR - 42, dy + 108, "กระแสจริงไหลลง", 12.5, B1, "end")
    s += txt(XR - 42, dy + 128, "(ผ่าน R₂, R₃)", 12.5, B1, "end")

    res = [("กระแสวงรอบ", "j_1 = [ (R_2+R_3)i_s - v_s ] / R_T", LOOP),
           ("กระแสกิ่งที่ 1", "i_1 = + j_1 = [ (R_2+R_3)i_s - v_s ] / R_T", B1),
           ("กระแสกิ่งที่ 2", "i_2 = - j_1 = [ v_s - (R_2+R_3)i_s ] / R_T", B2),
           ("แรงดันกิ่งทั้งสอง", "v_1 = v_2 = -(R_2+R_3)(v_s + R_1 i_s) / R_T", INK)]
    for k, (cap, eq, col) in enumerate(res):
        yy = 412 + 64 * k
        s += panel(50, yy, 840, 54, "#ffffff", "#e5e7eb")
        s += txt(74, yy + 33, cap, 14.5, col, "start", "700")
        s += M(270, yy + 35, eq, 18, INK, "start")
    s += txt(W / 2, 700, "เครื่องหมายลบของ v₁, v₂ มาจากการวางขั้ว + ไว้ที่ปม o", 13.5, MUTED)
    s += txt(W / 2, 722, "แรงดันของปม a เทียบปม o คือ  v(a) = (R₂+R₃)(v_s + R₁i_s) / R_T  ซึ่งเป็นบวก", 13.5, MUTED)
    s += tail()
    save("fig-07-results.svg", s)


# =====================================================================
# รูปที่ 8 — ตัวอย่างตัวเลขและการตรวจคำตอบ
# =====================================================================
def fig08():
    W, H = 940, 850
    dx, dy = 195, 150
    TOP, BOT = dy, dy + 220
    XL, XA, XR = dx, dx + 290, dx + 570
    s = head(W, H, "ตัวอย่างตัวเลขและการตรวจคำตอบ")
    s += txt(W / 2, 36, "รูปที่ 8 — แทนตัวเลขเพื่อทดสอบสูตร แล้วตรวจด้วยวิธีปมและสมดุลกำลัง", 20, INK, weight="700")
    s += txt(W / 2, 60, "กำหนด  R₁ = 2 Ω,  R₂ = 3 Ω,  R₃ = 5 Ω,  v_s = 10 V,  i_s = 4 A   ⇒   R_T = 10 Ω,  R₂+R₃ = 8 Ω", 14, MUTED)

    s += outer_loop(XL, XR, TOP, dy + 150, "j_1 = 2.2 A")
    s += base_circuit(dx, dy)
    s += txt(XL + 135, TOP - 18, "2 Ω", 15, INK, weight="600")
    s += txt(XA + 135, TOP - 18, "3 Ω", 15, INK, weight="600")
    s += txt(XR + 28, dy + 116, "5 Ω", 15, INK, "start", "600")
    s += txt(XL - 34, dy + 116, "10 V", 15, INK, "end", "600")
    s += txt(XA + 30, dy + 116, "4 A", 15, INK, "start", "600")
    s += node_dot(XA, TOP, 6, INK)
    s += node_dot(XA, BOT, 6, INK)
    s += M(XA - 14, TOP - 12, "a", 17, INK, "end", "700")
    s += M(XA - 14, BOT + 24, "o", 17, INK, "end", "700")
    s += txt(XA + 34, TOP + 40, "v(a) = 14.4 V", 14, SRC, "start", "700")

    s += arrow(XL + 30, dy + 55, XL + 30, dy + 175, B2, 2.4)
    s += txt(XL + 42, dy + 104, "2.2 A", 14, B2, "start", "700")
    s += txt(XL + 42, dy + 124, "(ผ่าน R₁ และ v_s)", 12, B2, "start")
    s += arrow(XR - 30, dy + 55, XR - 30, dy + 175, B1, 2.4)
    s += txt(XR - 42, dy + 104, "1.8 A", 14, B1, "end", "700")
    s += txt(XR - 42, dy + 124, "(ผ่าน R₂ และ R₃)", 12, B1, "end")

    s += panel(50, 412, 400, 168, "#ffffff", "#e2e8f0")
    s += txt(74, 442, "ตรวจที่ 1 — วิธีปม (KCL ที่ปม a)", 15, INK, "start", "700")
    s += M(74, 478, "[v(a) - v_s] / R_1 + v(a) / (R_2+R_3) = i_s", 16, INK, "start")
    s += txt(74, 512, "(14.4 − 10)/2 + 14.4/8 = 2.2 + 1.8 = 4 A", 15, INK, "start")
    s += txt(74, 546, "เท่ากับ i_s พอดี ✓", 15, B2, "start", "700")

    s += panel(490, 412, 400, 168, "#ffffff", "#e2e8f0")
    s += txt(514, 442, "ตรวจที่ 2 — แทนตัวเลขในสูตรที่ได้", 15, INK, "start", "700")
    s += txt(514, 478, "j₁ = (8 × 4 − 10) / 10 = 2.2 A", 15, INK, "start")
    s += txt(514, 512, "v₁ = v₂ = −8(10 + 2×4)/10 = −14.4 V", 15, INK, "start")
    s += txt(514, 546, "i₁ = +2.2 A ,  i₂ = −2.2 A ✓", 15, B2, "start", "700")

    s += panel(50, 606, 840, 212, "#f8fafc")
    s += txt(74, 636, "ตรวจที่ 3 — สมดุลกำลัง (กำลังที่จ่าย = กำลังที่ดูดกลืน)", 15, INK, "start", "700")
    x0, wtot, total = 90, 760, 57.6
    s += txt(74, 668, "จ่ายโดยแหล่งกำเนิดกระแส", 13, MUTED, "start")
    s += f'<rect x="{x0}" y="676" width="{wtot}" height="34" rx="6" fill="{SRC}"/>\n'
    s += txt(x0 + wtot / 2, 699, "i_s จ่าย  4 A × 14.4 V = 57.6 W", 14, "#fff", weight="700")
    s += txt(74, 744, "ถูกดูดกลืนโดย", 13, MUTED, "start")
    xx = x0
    for lab, pw, col in (("v_s  22 W", 22.0, "#b45309"), ("R₁  9.68 W", 9.68, "#0f766e"),
                         ("R₂  9.72 W", 9.72, "#1d4ed8"), ("R₃  16.2 W", 16.2, "#7e22ce")):
        w = wtot * pw / total
        s += f'<rect x="{xx:.1f}" y="752" width="{w:.1f}" height="34" rx="6" fill="{col}"/>\n'
        s += txt(xx + w / 2, 775, lab, 12.5, "#fff", weight="700")
        xx += w
    s += txt(W / 2, 806, "รวม 22 + 9.68 + 9.72 + 16.2 = 57.6 W  ตรงกับกำลังที่จ่าย ✓", 14, B2, weight="700")
    s += tail()
    save("fig-08-numeric-check.svg", s)


if __name__ == "__main__":
    fig01(); fig02(); fig03(); fig04(); fig05(); fig06(); fig07(); fig08()
    print("เสร็จสิ้น — สร้างรูปทั้งหมดในโฟลเดอร์ assets/")
