#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างรูป "การตัดชุดตัด (cut-set) บนกราฟมีทิศทางกำกับ" — โจทย์ข้อ 5

หลักการที่ยึด
-------------
1. เรขาคณิตของกราฟถอดสัดส่วนมาจากรูปที่ 5 (ข) ต้นฉบับ:
   a=(0,0), b=(1.00,0), e=(0.01,1.70), ยอดโค้งกิ่ง 1 = (-0.73,0.87)
2. เส้นตัดวาดตามธรรมเนียมในรูปตัวอย่างลายมือ: เส้นเปิดยาวพาดข้ามกราฟ
   ปลายโผล่พ้นตัวกราฟ ไม่ลากผ่านปม มีหัวลูกศรกำกับทิศ ป้ายชื่อที่ปลายอิสระ
3. "สิ่งที่วาด" กับ "สิ่งที่คำนวณ" ต้องเป็นเส้นเดียวกันเสมอ
   ทุกกิ่ง/ทุกเส้นตัดถูก sample เป็น polyline ชุดเดียว แล้วใช้ polyline นั้น
   ทั้งวาด SVG และคำนวณจุดตัด — ตัดปัญหา "รูปกับเลขไม่ตรงกัน" ที่ต้นเหตุ
4. ทุกข้ออ้างในรูปต้องพิสูจน์ได้ ไม่ใช่กะด้วยตา แล้ว assert:
   จุดตัด · ฝั่งที่ถูกล้อม (point-in-polygon) · ระยะห่างป้ายทุกคู่ · ระยะห่างจากเส้น
   ถ้าข้อใดพัง สคริปต์จะหยุด ไม่ปล่อยรูปผิดออกมา

ใช้ไลบรารีมาตรฐานล้วน (pure stdlib)
"""

import math
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ============================================================================
# 1) เรขาคณิตของกราฟ (ถอดสัดส่วนจากต้นฉบับ)
# ============================================================================
W, H = 1560, 1300
DRAW = (404, 118, 1512, 838)          # กรอบพื้นที่วาดกราฟ x0,y0,x1,y1

AX, AY = 812.0, 268.0
AB, AE, BULGE = 300.0, 510.0, 219.0

A = (AX, AY)
B = (AX + AB, AY)
E = (AX, AY + AE)

# วงกลมของกิ่ง 1 : คอร์ด a–e ยาว AE, ระยะปูดออกซ้าย BULGE
#   R = (s² + (c/2)²) / (2s)   ,  ศูนย์กลางเยื้องไปฝั่งตรงข้ามการปูด
ARC_R = (BULGE ** 2 + (AE / 2) ** 2) / (2 * BULGE)
ARC_C = (AX + ARC_R - BULGE, AY + AE / 2)
assert abs(math.dist(ARC_C, A) - ARC_R) < 1e-6
assert abs(math.dist(ARC_C, E) - ARC_R) < 1e-6
assert abs((ARC_C[0] - ARC_R) - (AX - BULGE)) < 1e-6

INK, BLUE, RED, PURPLE = "#101418", "#1a3a8f", "#b3202c", "#6a2fb5"
PURPLE_B = "#c0392b"
C1_COL, C2_COL = "#7b2cbf", "#0f7b8a"      # เส้นตัดคนละสี แยกกันชัด

# ============================================================================
# 2) เครื่องมือเรขาคณิต
# ============================================================================

def arc_polyline(n=300):
    """สุ่มจุดบนส่วนโค้งกิ่ง 1 จาก e ขึ้นไป a ผ่านยอดโค้งด้านซ้าย"""
    a0 = math.atan2(E[1] - ARC_C[1], E[0] - ARC_C[0])
    a1 = math.atan2(A[1] - ARC_C[1], A[0] - ARC_C[0])
    # ระบบพิกัด SVG แกน y ชี้ลง: ต้องกวาดมุมทาง "บวก" จึงจะอ้อมไปทางซ้าย
    while a1 < a0:
        a1 += 2 * math.pi
    pts = [(ARC_C[0] + ARC_R * math.cos(a0 + (a1 - a0) * i / n),
            ARC_C[1] + ARC_R * math.sin(a0 + (a1 - a0) * i / n))
           for i in range(n + 1)]
    assert abs(min(p[0] for p in pts) - (AX - BULGE)) < 1.0
    return pts


def catmull_rom(pts, per_seg=90):
    p = [pts[0]] + list(pts) + [pts[-1]]
    sampled = [pts[0]]
    for i in range(len(p) - 3):
        p0, p1, p2, p3 = p[i], p[i+1], p[i+2], p[i+3]
        c1 = (p1[0] + (p2[0]-p0[0])/6.0, p1[1] + (p2[1]-p0[1])/6.0)
        c2 = (p2[0] - (p3[0]-p1[0])/6.0, p2[1] - (p3[1]-p1[1])/6.0)
        for k in range(1, per_seg + 1):
            t = k / per_seg; mt = 1 - t
            sampled.append((
                mt**3*p1[0] + 3*mt*mt*t*c1[0] + 3*mt*t*t*c2[0] + t**3*p2[0],
                mt**3*p1[1] + 3*mt*mt*t*c1[1] + 3*mt*t*t*c2[1] + t**3*p2[1]))
    return sampled


def path_of(poly):
    """polyline -> svg path (เส้นที่วาด = เส้นที่คำนวณ เป๊ะ ๆ)"""
    d = f"M {poly[0][0]:.2f} {poly[0][1]:.2f}"
    for x, y in poly[1:]:
        d += f" L {x:.2f} {y:.2f}"
    return d


def seg_x(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(den) < 1e-12:
        return None
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    u = ((x1-x3)*(y1-y2) - (y1-y3)*(x1-x2)) / den
    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        return (x1 + t*(x2-x1), y1 + t*(y2-y1))
    return None


def crossings(pa, pb):
    out = []
    for i in range(len(pa) - 1):
        for j in range(len(pb) - 1):
            q = seg_x(pa[i], pa[i+1], pb[j], pb[j+1])
            if q and all(math.dist(q, o) > 2.0 for o in out):
                out.append(q)
    return out


def point_at(poly, frac):
    """จุดบน polyline ที่ระยะ frac (0..1) ของความยาวจริง
    ใช้ได้แม้ polyline มีแค่ 2 จุด (กิ่งเส้นตรง)"""
    segs = [math.dist(poly[i], poly[i+1]) for i in range(len(poly)-1)]
    tot = sum(segs)
    tgt, acc = tot * frac, 0.0
    for i, L in enumerate(segs):
        if acc + L >= tgt:
            t = (tgt - acc) / L if L else 0.0
            return (poly[i][0] + t*(poly[i+1][0]-poly[i][0]),
                    poly[i][1] + t*(poly[i+1][1]-poly[i][1]))
        acc += L
    return poly[-1]


def tangent_at(poly, pt):
    k = min(range(len(poly)-1), key=lambda i: math.dist(poly[i], pt))
    k = min(k, len(poly)-2)
    dx = poly[k+1][0]-poly[k][0]; dy = poly[k+1][1]-poly[k][1]
    n = math.hypot(dx, dy) or 1.0
    return dx/n, dy/n


def point_in_poly(pt, poly):
    x, y = pt; inside = False
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % len(poly)]
        if (y1 > y) != (y2 > y):
            if x < x1 + (y-y1)/(y2-y1)*(x2-x1):
                inside = not inside
    return inside


def dist_seg(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx-ax, by-ay
    L = dx*dx + dy*dy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((px-ax)*dx + (py-ay)*dy)/L))
    return math.dist(p, (ax+t*dx, ay+t*dy))


def dist_poly(p, poly):
    return min(dist_seg(p, poly[i], poly[i+1]) for i in range(len(poly)-1))


def poly_gap(pa, pb):
    """ระยะที่ใกล้ที่สุดระหว่างสอง polyline"""
    return min(min(dist_poly(p, pb) for p in pa),
               min(dist_poly(p, pa) for p in pb))


def extend_to_rect(poly, rect):
    """ต่อปลายทั้งสองของ polyline ตามแนวสัมผัส จนชนขอบกรอบ
    ใช้เฉพาะตอนคำนวณ 'ฝั่งที่ถูกล้อม' — เส้นที่วาดจริงยังสั้นอยู่ในกรอบ"""
    x0, y0, x1, y1 = rect
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

    def hit(p, d):
        far = (p[0] + d[0] * 1e5, p[1] + d[1] * 1e5)
        for c0, c1 in zip(corners, corners[1:] + corners[:1]):
            q = seg_x(p, far, c0, c1)
            if q:
                return q
        raise AssertionError("ต่อปลายไปไม่ถึงขอบกรอบ")

    def unit(p, q):
        dx, dy = p[0] - q[0], p[1] - q[1]
        n = math.hypot(dx, dy) or 1.0
        return (dx / n, dy / n)

    return ([hit(poly[0], unit(poly[0], poly[1]))] + list(poly)
            + [hit(poly[-1], unit(poly[-1], poly[-2]))])


def close_on_rect(poly, rect, inside_pt, outside_pts):
    """ปิด polyline (ที่ปลายแตะขอบกรอบแล้ว) ด้วยมุมของกรอบ
    ให้ได้รูปปิดที่ครอบ inside_pt เท่านั้น"""
    x0, y0, x1, y1 = rect
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

    def perim(p):
        x, y = p
        if abs(y - y0) < 1e-6: return (x - x0) / (x1 - x0)
        if abs(x - x1) < 1e-6: return 1 + (y - y0) / (y1 - y0)
        if abs(y - y1) < 1e-6: return 2 + (x1 - x) / (x1 - x0)
        return 3 + (y1 - y) / (y1 - y0)

    t_tail, t_head = perim(poly[-1]), perim(poly[0])
    span_fwd = (t_head - t_tail) % 4

    for direction in (+1, -1):
        walk = []
        if direction > 0:
            k = math.ceil(t_tail)
            while (k - t_tail) % 4 < span_fwd and len(walk) < 5:
                walk.append(corners[int(k) % 4]); k += 1
        else:
            k = math.floor(t_tail)
            span_bwd = (t_tail - t_head) % 4
            while (t_tail - k) % 4 < span_bwd and len(walk) < 5:
                walk.append(corners[int(k) % 4]); k -= 1
        cand = list(poly) + walk
        if (point_in_poly(inside_pt, cand)
                and not any(point_in_poly(o, cand) for o in outside_pts)):
            return cand
    raise AssertionError("ปิดรูปฝั่งที่ล้อมไม่สำเร็จ")


# ============================================================================
# 3) กิ่งทั้งสี่ — ทิศลูกศรยึดตามต้นฉบับ
# ============================================================================
BR = {
    1: dict(poly=arc_polyline(), color=INK, kind="link", w=4.4,
            elem="G₁ อนุกรม E₁", ends="e → a"),
    2: dict(poly=[A, B], color=BLUE, kind="link", w=4.4,
            elem="E₃ อนุกรม G₂", ends="a → b"),
    3: dict(poly=[A, E], color=RED, kind="twig", w=7.8,
            elem="G₃", ends="a → e"),
    4: dict(poly=[E, B], color=RED, kind="twig", w=7.8,
            elem="G₄ ขนาน E₂", ends="e → b"),
}
NODE = {"a": A, "b": B, "e": E}


def rel(x, y):
    return (AX + x, AY + y)


# ============================================================================
# 4) เส้นตัด : c₁ ล้อมปม a (ตัด 1,2,3) · c₂ ล้อมปม b (ตัด 2,4)
# ============================================================================
CUTS = {
    "c₁": dict(node="a", col=C1_COL, dash="17 11",
               pts=[rel(150, -128), rel(112, 26), rel(58, 152),
                    rel(-70, 192), rel(-196, 74), rel(-346, -74)],
               expect={1: -1, 2: +1, 3: +1},
               kcl="− i₁ + i₂ + i₃ = 0",
               row="แถวที่ 1 ของ Q  =  [ −1   +1   +1    0 ]",
               cuts_txt="ตัดกิ่ง 1, 2, 3", lab=(-38, -18)),
    "c₂": dict(node="b", col=C2_COL, dash="24 9 5 9",
               pts=[rel(232, -128), rel(214, 66), rel(244, 198), rel(338, 330)],
               expect={2: -1, 4: -1},
               kcl="− i₂ − i₄ = 0     (i₄ = i_G₄ + i_E₂)",
               row="แถวที่ 2 ของ Q  =  [  0   −1    0   −1 ]",
               cuts_txt="ตัดกิ่ง 2, 4", lab=(34, 30)),
}

for name, c in CUTS.items():
    c["poly"] = catmull_rom(c["pts"])

    hits = {}
    for bn, br in BR.items():
        xs = crossings(c["poly"], br["poly"])
        if xs:
            assert len(xs) == 1, f"{name} ตัดกิ่ง {bn} ซ้ำ {len(xs)} ครั้ง"
            hits[bn] = xs[0]
    assert set(hits) == set(c["expect"]), \
        f"{name}: ตัดกิ่ง {sorted(hits)} แต่ประกาศ {sorted(c['expect'])}"
    c["hits"] = hits

    for nm, xy in NODE.items():
        d = dist_poly(xy, c["poly"])
        assert d > 46, f"{name} เฉียดปม {nm} ({d:.0f}px)"

    others = [xy for nm, xy in NODE.items() if nm != c["node"]]
    c["region"] = close_on_rect(extend_to_rect(c["poly"], DRAW), DRAW,
                                NODE[c["node"]], others)

    # ปลายทั้งสองต้องอยู่ในกรอบวาด (ไม่วิ่งชนหัวเรื่อง / ไม่ถูกตัดขอบ)
    for p in (c["poly"][0], c["poly"][-1]):
        assert DRAW[0]+6 < p[0] < DRAW[2]-6 and DRAW[1]+6 < p[1] < DRAW[3]-6, \
            f"{name} ปลายเส้นหลุดกรอบวาด {p}"

assert poly_gap(CUTS["c₁"]["poly"], CUTS["c₂"]["poly"]) > 40, "เส้นตัดสองเส้นเบียดกัน"

Q = [[CUTS["c₁"]["expect"].get(b, 0) for b in (1, 2, 3, 4)],
     [CUTS["c₂"]["expect"].get(b, 0) for b in (1, 2, 3, 4)]]
assert Q == [[-1, 1, 1, 0], [0, -1, 0, -1]], Q

# ---- วางป้าย ±1 (สองบรรทัดในกล่องเดียว ไม่มีคำบรรยายลอย) ----
BW, BH = 74, 52
placed = []
for name, c in CUTS.items():
    for bn, (cx, cy) in sorted(c["hits"].items()):
        tx, ty = tangent_at(BR[bn]["poly"], (cx, cy))
        px, py = -ty, tx
        best = None
        for sgn in (+1, -1):
            for off in (52, 66, 82, 100, 120):
                bx, by = cx + px*sgn*off, cy + py*sgn*off
                if not (DRAW[0]+BW/2+8 < bx < DRAW[2]-BW/2-8
                        and DRAW[1]+BH/2+8 < by < DRAW[3]-BH/2-8):
                    continue
                s = 0.0
                s += 3.0*max(0.0, 118 - min(math.dist((bx, by), v) for v in NODE.values()))
                for ob in [b["poly"] for b in BR.values()] + [q["poly"] for q in CUTS.values()]:
                    s += 4.0*max(0.0, 52 - dist_poly((bx, by), ob))
                for _, _, ox, oy in placed:
                    s += 11.0*max(0.0, 104 - math.hypot(bx-ox, by-oy))
                s += 0.4*off
                if best is None or s < best[0]:
                    best = (s, bx, by)
        assert best, f"หาที่วางป้าย {name}×{bn} ไม่ได้"
        placed.append((name, bn, best[1], best[2]))

for i in range(len(placed)):
    for j in range(i+1, len(placed)):
        d = math.hypot(placed[i][2]-placed[j][2], placed[i][3]-placed[j][3])
        assert d > 92, (f"ป้าย {placed[i][0]}×{placed[i][1]} ชน "
                        f"{placed[j][0]}×{placed[j][1]} ({d:.0f}px)")

# ---- วางเลขกำกับกิ่ง : ยึดกลางกิ่ง โดยระยะห่างจากปมเป็น "เงื่อนไขบังคับ" ----
MIN_NODE_GAP = 96.0          # เลขกิ่งต้องห่างจากทุกปมอย่างน้อยเท่านี้

NUMPOS = {}
for bn, br in BR.items():
    poly = br["poly"]
    best = None
    for t in (0.40, 0.45, 0.50, 0.55, 0.60):
        base = point_at(poly, t)
        tx, ty = tangent_at(poly, base)
        px, py = -ty, tx
        for sgn in (+1, -1):
            for off in (34, 44, 56, 70, 84):
                nx, ny = base[0] + px*sgn*off, base[1] + py*sgn*off
                if not (DRAW[0]+20 < nx < DRAW[2]-20 and DRAW[1]+20 < ny < DRAW[3]-20):
                    continue
                # เงื่อนไขบังคับ: ห้ามเข้าใกล้ปมเกินกำหนด (กันชนกับตัวอักษร a/b/e)
                if min(math.dist((nx, ny), v) for v in NODE.values()) < MIN_NODE_GAP:
                    continue
                sc = 60.0 * abs(t - 0.5)                  # ชอบกึ่งกลางกิ่ง
                for ob in ([b["poly"] for b in BR.values()]
                           + [q["poly"] for q in CUTS.values()]):
                    sc += 3.0 * max(0.0, 30 - dist_poly((nx, ny), ob))
                for _, _, ox, oy in placed:
                    sc += 8.0 * max(0.0, 76 - math.hypot(nx-ox, ny-oy))
                sc += 0.25 * off
                if best is None or sc < best[0]:
                    best = (sc, nx, ny)
    assert best, f"วางเลขกิ่ง {bn} ไม่ได้ภายใต้เงื่อนไขระยะห่างจากปม"
    NUMPOS[bn] = (best[1], best[2])

for bn, (nx, ny) in NUMPOS.items():
    dn = min(math.dist((nx, ny), v) for v in NODE.values())
    assert dn >= MIN_NODE_GAP, f"เลขกิ่ง {bn} ใกล้ปมเกินไป ({dn:.0f}px)"
    for _, _, ox, oy in placed:
        assert math.hypot(nx-ox, ny-oy) > 46, f"เลขกิ่ง {bn} ชนป้าย ±1"

# ============================================================================
# 5) วาด SVG
# ============================================================================
TH = "'Sarabun','Noto Sans Thai','IBM Plex Sans Thai',Thonburi,system-ui,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
out = []
add = out.append


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=15, fill="#22303f", anchor="start", weight="normal",
         family=TH, style="normal"):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" font-style="{style}" fill="{fill}" '
        f'text-anchor="{anchor}">{esc(s)}</text>')


def rrect(x, y, w, h, r, fill, stroke="none", sw=0):
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def arrow_on(poly, frac, color, size=15.0):
    tot = sum(math.dist(poly[i], poly[i+1]) for i in range(len(poly)-1))
    tgt, acc = tot*frac, 0.0
    for i in range(len(poly)-1):
        seg = math.dist(poly[i], poly[i+1])
        if acc + seg >= tgt:
            t = (tgt-acc)/seg
            px = poly[i][0] + t*(poly[i+1][0]-poly[i][0])
            py = poly[i][1] + t*(poly[i+1][1]-poly[i][1])
            dx = (poly[i+1][0]-poly[i][0])/seg; dy = (poly[i+1][1]-poly[i][1])/seg
            nx, ny = -dy, dx
            add(f'<path d="M {px+dx*size:.1f} {py+dy*size:.1f} '
                f'L {px-dx*size*.5+nx*size*.6:.1f} {py-dy*size*.5+ny*size*.6:.1f} '
                f'L {px-dx*size*.5-nx*size*.6:.1f} {py-dy*size*.5-ny*size*.6:.1f} Z" '
                f'fill="{color}"/>')
            return
        acc += seg


add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add(f'<defs><clipPath id="draw"><rect x="{DRAW[0]}" y="{DRAW[1]}" '
    f'width="{DRAW[2]-DRAW[0]}" height="{DRAW[3]-DRAW[1]}"/></clipPath></defs>')
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

rrect(0, 0, W, 100, 0, "#f2f7ff")
add(f'<rect x="0" y="98" width="{W}" height="2" fill="#d6e4f5"/>')
text(W/2, 42, "การตัดชุดตัด (Cut-set) บนกราฟมีทิศทางกำกับ — รูปที่ 5 (ข)",
     size=29, fill="#0b2545", anchor="middle", weight="bold")
text(W/2, 76, "ต้นไม้ tree = {3, 4} เส้นหนา · ลิงก์ link = {1, 2} เส้นบาง · "
              "อ่านป้าย ±1 ที่จุดตัด เรียงตามกิ่ง 1→4 ได้เป็นแถวของเมทริกซ์ Q",
     size=16.5, fill="#41566e", anchor="middle")

# ---- พื้นที่ที่ถูกล้อม (clip ให้อยู่แต่ในกรอบวาด) ----
add('<g clip-path="url(#draw)">')
for name in ("c₂", "c₁"):
    c = CUTS[name]
    add(f'<path d="{path_of(c["region"])} Z" fill="{c["col"]}" opacity="0.075"/>')
add('</g>')

# ---- กิ่ง (วาดจาก polyline ชุดเดียวกับที่ใช้คำนวณ) ----
for bn, br in BR.items():
    add(f'<path d="{path_of(br["poly"])}" fill="none" stroke="{br["color"]}" '
        f'stroke-width="{br["w"]}" stroke-linecap="round" stroke-linejoin="round"/>')
for bn, frac in ((1, 0.50), (2, 0.50), (3, 0.55), (4, 0.50)):
    arrow_on(BR[bn]["poly"], frac, BR[bn]["color"])
for bn, (nx, ny) in NUMPOS.items():
    add(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="19" fill="#ffffff" opacity="0.92"/>')
    text(nx, ny+10, str(bn), size=29, fill=BR[bn]["color"], family=SERIF,
         style="italic", anchor="middle", weight="bold")

# ---- เส้นตัด ----
for name, c in CUTS.items():
    add(f'<path d="{path_of(c["poly"])}" fill="none" stroke="{c["col"]}" '
        f'stroke-width="4.8" stroke-linecap="round" stroke-dasharray="{c["dash"]}"/>')
    arrow_on(c["poly"], 0.999, c["col"], size=17)
    ex, ey = c["poly"][-1]
    text(ex+c["lab"][0], ey+c["lab"][1], name, size=30, fill=c["col"],
         weight="bold", family=SERIF, style="italic", anchor="middle")

# ---- × + ป้าย ±1 ----
for name, bn, bx, by in placed:
    c = CUTS[name]; cx, cy = c["hits"][bn]
    tx, ty = tangent_at(c["poly"], (cx, cy))
    ang = math.degrees(math.atan2(ty, tx))
    add(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
        f'stroke="{c["col"]}" stroke-width="1.8" stroke-dasharray="3 3" opacity="0.85"/>')
    add(f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})" '
        f'stroke="{c["col"]}" stroke-width="3.8" stroke-linecap="round">'
        f'<line x1="-10" y1="-10" x2="10" y2="10"/>'
        f'<line x1="10" y1="-10" x2="-10" y2="10"/></g>')
    rrect(bx-BW/2-3, by-BH/2-3, BW+6, BH+6, 12, "#ffffff")
    rrect(bx-BW/2, by-BH/2, BW, BH, 10, "#ffffff", c["col"], 2.4)
    s = c["expect"][bn]
    text(bx, by-2, f'{"+" if s > 0 else "−"}1', size=20, fill=c["col"],
         weight="bold", anchor="middle")
    text(bx, by+18, f'{name} · กิ่ง {bn}', size=12.5, fill=c["col"], anchor="middle")

# ---- ปม ----
for nm, (x, y) in NODE.items():
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#ffffff"/>')
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11.5" fill="{INK}"/>')
text(A[0]-32, A[1]-20, "a", size=32, fill=INK, family=SERIF, style="italic", anchor="middle")
text(B[0]+28, B[1]-20, "b", size=32, fill=INK, family=SERIF, style="italic", anchor="middle")
text(E[0]+38, E[1]+8, "e", size=32, fill=INK, family=SERIF, style="italic", anchor="middle")
gx, gy = E
add(f'<g stroke="{INK}" stroke-width="4" stroke-linecap="round">'
    f'<line x1="{gx}" y1="{gy+12}" x2="{gx}" y2="{gy+38}"/>'
    f'<line x1="{gx-33}" y1="{gy+38}" x2="{gx+33}" y2="{gy+38}"/>'
    f'<line x1="{gx-21}" y1="{gy+50}" x2="{gx+21}" y2="{gy+50}"/>'
    f'<line x1="{gx-9}" y1="{gy+62}" x2="{gx+9}" y2="{gy+62}"/></g>')
text(gx+54, gy+56, "ปมอ้างอิง  Vₑ = 0 V", size=15, fill="#5b6f85")

# ---- การ์ดซ้าย : กิ่ง ----
LX, LY, LW = 62, 150, 316
rrect(LX, LY, LW, 262, 14, "#fbfdff", "#c3d5ea", 2)
text(LX+20, LY+36, "กิ่งในกราฟ", size=18, fill="#0b2545", weight="bold")
add(f'<line x1="{LX+20}" y1="{LY+50}" x2="{LX+LW-20}" y2="{LY+50}" stroke="#dbe6f3" stroke-width="1.6"/>')
for i, bn in enumerate((1, 2, 3, 4)):
    br = BR[bn]; yy = LY + 86 + i*44
    add(f'<line x1="{LX+22}" y1="{yy-6}" x2="{LX+62}" y2="{yy-6}" '
        f'stroke="{br["color"]}" stroke-width="{br["w"]}" stroke-linecap="round"/>')
    text(LX+74, yy, f"{bn}.", size=17, fill=br["color"], weight="bold",
         family=SERIF, style="italic")
    text(LX+96, yy, br["elem"], size=14.5, fill="#22303f")
    text(LX+96, yy+17, br["ends"], size=12.5, fill="#7d8fa3", family=SERIF, style="italic")
    text(LX+LW-18, yy, "twig" if br["kind"] == "twig" else "link", size=12.5,
         fill=(RED if br["kind"] == "twig" else "#41566e"), anchor="end")

# ---- การ์ดซ้าย : วิธีอ่าน ----
NX, NY = 62, 434
rrect(NX, NY, LW, 214, 14, "#faf7ff", "#b9a0d8", 2)
text(NX+20, NY+34, "อ่านรูปนี้อย่างไร", size=18, fill="#4a235a", weight="bold")
add(f'<line x1="{NX+20}" y1="{NY+48}" x2="{NX+LW-20}" y2="{NY+48}" stroke="#e6d5f2" stroke-width="1.6"/>')
for i, (sw, s) in enumerate([
        (C1_COL, "เส้นประ = เส้นตัด พาดข้ามกิ่ง"),
        (C2_COL, "พื้นสีจาง = ฝั่งที่ถูกล้อมไว้"),
        (None, "× = จุดที่เส้นตัดข้ามกิ่ง"),
        (None, "+1 = ลูกศรออกจากฝั่งที่ล้อม"),
        (None, "−1 = ลูกศรเข้าสู่ฝั่งที่ล้อม")]):
    yy = NY + 80 + i*27
    if sw:
        add(f'<line x1="{NX+22}" y1="{yy-5}" x2="{NX+44}" y2="{yy-5}" stroke="{sw}" '
            f'stroke-width="3.6" stroke-dasharray="7 5" stroke-linecap="round"/>')
        text(NX+52, yy, s, size=13.5, fill="#4a235a")
    else:
        text(NX+22, yy, "• " + s, size=13.5, fill="#4a235a")

# ---- การ์ดสรุปแต่ละ cut ----
PY0 = 872
for i, (name, c) in enumerate(CUTS.items()):
    px = 62 + i*730
    rrect(px, PY0, 706, 110, 12, "#fcfaff", c["col"], 2.2)
    text(px+22, PY0+34, f'เส้นตัด {name} — {c["cuts_txt"]}  (ล้อมปม {c["node"]})',
         size=17.5, fill="#3b2352", weight="bold")
    text(px+22, PY0+64, f'KCL :  {c["kcl"]}', size=16.5, fill="#3b2352")
    text(px+22, PY0+93, c["row"], size=15.5, fill=c["col"])

# ---- การ์ดผลลัพธ์ ----
RY = 1004
rrect(62, RY, 1436, 196, 12, "#fbfdff", "#b7c9e2", 2)
text(84, RY+36, "อ่านจากรูป :   Q = [ −1  +1  +1   0 ;   0  −1   0  −1 ]        "
                "Y_b = diag(G₁, G₂, G₃, G₄)", size=16.5, fill="#0b2545", weight="bold")
text(84, RY+68, "⇒   Q · Y_b · Qᵀ  =  [ G₁+G₂+G₃    −G₂ ;    −G₂    G₂+G₄ ]        "
                "(สมมาตรเสมอ เพราะ Y_b สมมาตร)", size=16.5, fill="#22303f")
add(f'<line x1="84" y1="{RY+90}" x2="1476" y2="{RY+90}" stroke="#dbe6f3" stroke-width="1.6"/>')
text(84, RY+122, "ระบบที่แก้ได้จริง :   (G₁+G₂+G₃)·V_a − G₂·V_b = G₁E₁ − G₂E₃        "
                 "และ        V_b = −E₂", size=17, fill="#22303f", weight="bold")
text(84, RY+152, "เครื่องหมาย −G₂E₃ มาจากขั้ว E₃ ในรูป (ลบอยู่ฝั่งปม a บวกอยู่ฝั่ง G₂) "
                 "จึงได้ i₂ = G₂(V_a + E₃ − V_b)", size=14, fill="#5b6f85")
text(84, RY+178, "กิ่ง 4 เป็นกิ่งรวม (G₄ ขนาน E₂) : i₄ = i_G₄ + i_E₂ — แถวของ c₂ จึงมีสองพจน์ตรงกับป้ายสองใบ "
                 "ส่วนที่ใช้แก้ระบบคือเงื่อนไข V_b = −E₂ (แหล่งอุดมคติตรึงปม b)", size=14, fill="#5b6f85")

add('</svg>')

svg = HERE / "cut_set_detailed.svg"
svg.write_text("\n".join(out), encoding="utf-8")
png = HERE / "cut_set_detailed.png"
subprocess.run(["rsvg-convert", "-w", str(W*2), "-o", str(png), str(svg)], check=True)

print("✓ ตรวจผ่านทุกข้อ (เรขาคณิต · ฝั่งที่ล้อม · ระยะห่างป้าย)")
print(f"✓ {svg.name}\n✓ {png.name}\n")
print(f"arc: center=({ARC_C[0]:.1f},{ARC_C[1]:.1f})  R={ARC_R:.1f}  "
      f"ซ้ายสุด x={ARC_C[0]-ARC_R:.1f} (ควร = {AX-BULGE:.1f})")
print("\nจุดตัดที่พิสูจน์แล้ว:")
for name, bn, bx, by in placed:
    cx, cy = CUTS[name]["hits"][bn]
    on = abs(math.dist(ARC_C, (cx, cy)) - ARC_R) < 1.0 if bn == 1 else True
    print(f"   {name} × กิ่ง {bn}  ที่ ({cx:7.1f},{cy:7.1f})  "
          f"ป้าย {CUTS[name]['expect'][bn]:+d} ที่ ({bx:7.1f},{by:7.1f})"
          f"{'  [อยู่บนส่วนโค้งจริง ✓]' if bn == 1 and on else ''}")
mind = min(math.hypot(placed[i][2]-placed[j][2], placed[i][3]-placed[j][3])
           for i in range(len(placed)) for j in range(i+1, len(placed)))
print(f"\nระยะห่างป้ายที่ใกล้ที่สุด = {mind:.1f} px (ต้อง > 92)")
print(f"Q = {Q}")
