#!/usr/bin/env python3
"""Generate eight vector SVG teaching figures for circuit problem 4.6.

Run from any directory:
    python3 engineering-problem/circuit/2/chapter4/4.6/make_figures.py

The script uses only the Python standard library. SVG text remains searchable
and all diagrams stay sharp at arbitrary zoom levels.
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
MARKERS = {INK:"ink", BLUE:"blue", RED:"red", GREEN:"green", PURPLE:"purple",
           AMBER:"amber", CYAN:"cyan", PINK:"pink"}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def head(width: int, height: int, title: str) -> str:
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


def text(x: float, y: float, value: object, size: float = 18, color: str = INK,
         anchor: str = "middle", weight: int = 400, family: str = FONT) -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}" font-family="{family}">'
            f'{esc(value)}</text>\n')


def lines(x: float, y: float, values: list[str], size: float = 17, color: str = INK,
          anchor: str = "start", gap: float = 28, weight: int = 400,
          family: str = FONT) -> str:
    return "".join(text(x, y+i*gap, value, size, color, anchor, weight, family)
                   for i, value in enumerate(values))


def math_text(x: float, y: float, value: object, size: float = 20, color: str = INK,
              anchor: str = "middle", weight: int = 400) -> str:
    return text(x, y, value, size, color, anchor, weight, MATH)


def rect(x: float, y: float, width: float, height: float, fill: str = PAPER,
         stroke: str = GRID, radius: float = 18, stroke_width: float = 1.5,
         dash: str | None = None) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{dashed}/>\n')


def line(x1: float, y1: float, x2: float, y2: float, color: str = INK,
         width: float = 2.7, dash: str | None = None) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round"{dashed}/>\n')


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = BLUE,
          width: float = 2.7, dash: str | None = None) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" '
            f'marker-end="url(#arr-{MARKERS[color]})"{dashed}/>\n')


def path(d: str, color: str = INK, width: float = 2.7, fill: str = "none",
         arrow_end: bool = False, dash: str | None = None) -> str:
    marker = f' marker-end="url(#arr-{MARKERS[color]})"' if arrow_end else ""
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{marker}{dashed}/>\n')


def circle(cx: float, cy: float, radius: float, fill: str = PAPER,
           stroke: str = INK, width: float = 2.4) -> str:
    return (f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{width}"/>\n')


def node(x: float, y: float, label: str | None = None, dx: float = 0, dy: float = -17) -> str:
    out = circle(x, y, 7, INK, INK, 1)
    if label:
        out += math_text(x+dx, y+dy, label, 21, INK, "middle", 700)
    return out


def resistor_points(x1: float, y1: float, x2: float, y2: float,
                    amplitude: float = 11, turns: int = 7) -> str:
    dx, dy = x2-x1, y2-y1
    length = math.hypot(dx, dy)
    ux, uy = dx/length, dy/length
    px, py = -uy, ux
    pts = [(x1, y1)]
    for k in range(1, turns*2):
        step = length*k/(turns*2)
        sign = 1 if k % 2 else -1
        pts.append((x1+ux*step+px*amplitude*sign, y1+uy*step+py*amplitude*sign))
    pts.append((x2, y2))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def resistor(x1: float, y1: float, x2: float, y2: float, label: str,
             color: str = INK, label_x: float | None = None,
             label_y: float | None = None) -> str:
    out = (f'<polyline points="{resistor_points(x1,y1,x2,y2)}" fill="none" '
           f'stroke="{color}" stroke-width="2.8" stroke-linejoin="round"/>\n')
    lx = (x1+x2)/2 if label_x is None else label_x
    ly = (y1+y2)/2-20 if label_y is None else label_y
    return out + math_text(lx, ly, label, 21, color, "middle", 700)


def inductor(x: float, y1: float, y2: float, label: str = "L") -> str:
    lead = 36
    out = line(x, y1, x, y1+lead)
    top, bottom = y1+lead, y2-lead
    span = (bottom-top)/4
    d = f"M {x} {top} "
    for k in range(4):
        yy = top+k*span
        d += f"C {x+23} {yy+span*.18}, {x+23} {yy+span*.82}, {x} {yy+span} "
    out += path(d, INK, 2.8)
    out += line(x, bottom, x, y2)
    out += math_text(x+42, (y1+y2)/2+5, label, 21, INK, "start", 700)
    return out


def capacitor(x1: float, y: float, x2: float, label: str = "C") -> str:
    mid = (x1+x2)/2
    out = line(x1, y, mid-10, y)
    out += line(mid-10, y-25, mid-10, y+25, INK, 3.3)
    out += line(mid+10, y-25, mid+10, y+25, INK, 3.3)
    out += line(mid+10, y, x2, y)
    out += math_text(mid, y-42, label, 21, INK, "middle", 700)
    return out


def current_source(cx: float, cy: float, up: bool = True, label: str = "Iₛ",
                   color: str = BLUE) -> str:
    out = circle(cx, cy, 30, PAPER, color, 2.7)
    out += arrow(cx, cy+15 if up else cy-15, cx, cy-15 if up else cy+15, color, 2.5)
    out += math_text(cx-43, cy+6, label, 19, color, "end", 700)
    return out


def voltage_source(cx: float, cy: float, label: str = "Vₛ", color: str = PURPLE) -> str:
    out = circle(cx, cy, 31, PAPER, color, 2.7)
    out += line(cx-8, cy-11, cx+8, cy-11, color, 2.4)
    out += line(cx, cy-19, cx, cy-3, color, 2.4)
    out += line(cx-8, cy+12, cx+8, cy+12, color, 2.4)
    out += math_text(cx+44, cy+6, label, 19, color, "start", 700)
    return out


def pill(x: float, y: float, width: float, label: str, color: str) -> str:
    return rect(x, y, width, 38, color, color, 19, 1) + text(x+width/2, y+25, label, 14, PAPER, "middle", 700)


def title_block(title: str, subtitle: str, width: int) -> str:
    return (text(54,55,title,29,INK,"start",800)+text(54,86,subtitle,16,MUTED,"start")+
            line(54,105,width-54,105,GRID,1.5))


def save(name: str, body: str, width: int, height: int, title: str) -> None:
    (OUT/name).write_text(head(width,height,title)+body+"</svg>\n", encoding="utf-8")


def fig01() -> None:
    w,h=1200,690
    b=title_block("แผนที่การแก้โจทย์ AC Tie-set", "โดเมนเวลา → phasor → topology → complex matrix → เวลา", w)
    cards=[("1","แปลง phasor",["cosine reference","Vₛ=V₀","Iₛ=−jI₀"],BLUE),
           ("2","อ่าน tree",["T={3,4}","L={1,2}","สร้าง B 2×4"],RED),
           ("3","Branch model",["ZC=−jXc","ZL=+jXl","Vs / Is vectors"],PURPLE),
           ("4","Matrix engine",["BZBᵀ","BZIₛ−BVₛ","solve 2×2"],GREEN),
           ("5","คืนคำตอบ",["I₁…I₄","V₁…V₄","A cos(ωt+φ)"],AMBER)]
    xs=[55,290,525,760,995]
    for x,(n,heading,details,color) in zip(xs,cards):
        b+=rect(x,155,180,245,SOFT,GRID)
        b+=circle(x+36,195,20,color,color,1)+text(x+36,202,n,17,PAPER,"middle",800)
        b+=text(x+20,250,heading,18,INK,"start",700)+lines(x+20,293,details,15,MUTED,"start",30)
    for x in [245,480,715,950]: b+=arrow(x,277,x+32,277,CYAN,3)
    b+=rect(130,465,940,145,"#eff6ff",BLUE,20,1.7)+pill(160,490,170,"VERIFY 5 มุม",BLUE)
    b+=lines(160,560,["KVL + KCL","Nodal analysis"],16,INK,"start",29,600)
    b+=lines(470,560,["ω→0, ω→∞","sources → 0"],16,INK,"start",29,600)
    b+=lines(790,560,["Complex power","Tellegen"],16,INK,"start",29,600)
    save("fig-01-roadmap.svg",b,w,h,"แผนที่การแก้โจทย์ AC tie-set")


def draw_circuit(phasor: bool = False) -> str:
    b=""
    A,B,O=(300,245),(720,245),(510,625)
    b+=line(170,625,970,625)+line(170,245,A[0],245)+line(B[0],245,820,245)
    b+=line(170,245,170,340)+current_source(170,420,True,"−jI₀" if phasor else "I₀ sin ωt",BLUE)+line(170,450,170,625)
    b+=line(A[0],245,A[0],330)+resistor(A[0],330,A[0],520,"R₂",INK,A[0]+42,430)+line(A[0],520,A[0],625)
    b+=capacitor(A[0],245,B[0],"ZC=−jXC" if phasor else "C")
    b+=line(B[0],245,B[0],330)+inductor(B[0],330,520,"ZL=+jXL" if phasor else "L")+line(B[0],520,B[0],625)
    b+=resistor(820,245,970,245,"R₁",INK,895,210)+line(970,245,970,340)+voltage_source(970,420,"V₀" if phasor else "V₀ cos ωt",PURPLE)+line(970,451,970,625)
    b+=node(*A,"A",0,-20)+node(*B,"B",0,-20)+node(*O,"O",0,32)
    b+=arrow(830,210,935,210,RED,2.6)+math_text(882,193,"I₁",18,RED,"middle",700)
    b+=arrow(335,340,335,485,BLUE,2.6)+math_text(352,417,"I₂",18,BLUE,"start",700)
    b+=arrow(405,205,615,205,GREEN,2.6)+math_text(510,187,"I₃",18,GREEN,"middle",700)
    b+=arrow(755,340,755,485,AMBER,2.6)+math_text(773,417,"I₄",18,AMBER,"start",700)
    return b


def fig02() -> None:
    w,h=1200,800
    b=title_block("อ่านปมและกิ่งจากรูปจริง", "ลูกศรสีคือทิศอ้างอิงของ I₁, I₂, I₃, I₄",w)
    b+=rect(45,135,1110,570,SOFT,GRID)+draw_circuit(False)
    b+=rect(95,720,1010,52,"#eff6ff",BLUE,13,1.5)
    b+=text(600,753,"1: B→O (R₁+Vₛ)   ·   2: A→O (R₂∥Iₛ)   ·   3: A→B (C)   ·   4: B→O (L)",16,INK,"middle",650)
    save("fig-02-circuit-anatomy.svg",b,w,h,"วงจรจริง ปม และทิศกระแสกิ่ง")


def fig03() -> None:
    w,h=1200,800
    b=title_block("วงจรสมมูลในโดเมนความถี่", "cosine reference และ peak phasor",w)
    b+=rect(45,135,1110,570,"#faf5ff",PURPLE)+draw_circuit(True)
    b+=rect(80,720,1040,54,SOFT,GRID,13)
    b+=math_text(600,755,"Vₛ=V₀∠0°   ·   Iₛ(up)=I₀∠−90°=−jI₀   ·   Iₛ(branch 2)=+jI₀",18,INK,"middle",700)
    save("fig-03-phasor-circuit.svg",b,w,h,"วงจรสมมูลในโดเมนเฟสเซอร์")


def fig04() -> None:
    w,h=1200,750
    b=title_block("Tree, Links และการอ่าน B", "T={3,4}; เติม link 1 และ link 2 ทีละกิ่ง",w)
    b+=rect(50,140,490,530,SOFT,GRID)+text(80,180,"กราฟและ tree",20,INK,"start",700)
    A,B,O=(130,330),(450,330),(290,590)
    b+=line(A[0],A[1],B[0],B[1],INK,6)+line(B[0],B[1],O[0],O[1],INK,6)
    b+=path(f"M {B[0]} {B[1]} L {O[0]} {O[1]}",RED,4,"none",False,"10 8")
    b+=path(f"M {A[0]} {A[1]} L {O[0]} {O[1]}",BLUE,4,"none",False,"10 8")
    b+=node(*A,"A",0,-22)+node(*B,"B",0,-22)+node(*O,"O",0,32)
    b+=pill(250,295,80,"3 twig",INK)+pill(350,445,80,"4 twig",INK)
    b+=pill(360,500,90,"1 link",RED)+pill(145,500,90,"2 link",BLUE)
    b+=path("M 428 360 C 390 430, 345 515, 305 558",RED,3,"none",True)
    b+=path("M 275 565 C 220 525, 165 420, 145 355",BLUE,3,"none",True)
    b+=path("M 150 300 C 220 250, 360 250, 430 300",BLUE,3,"none",True)
    b+=math_text(395,420,"J₁",21,RED,"middle",700)+math_text(235,270,"J₂",21,BLUE,"middle",700)
    b+=rect(575,140,575,530,PAPER,GRID)+text(605,180,"อ่านสมาชิกทีละแถว",20,INK,"start",700)
    rows=[(225,"Loop 1","[ +1   0    0   −1 ]",RED),(330,"Loop 2","[  0   +1  −1   −1 ]",BLUE)]
    for y,label,value,color in rows:
        b+=rect(610,y,505,78,SOFT,color,13,1.5)+pill(630,y+20,105,label,color)+math_text(925,y+50,value,22,INK,"middle",700)
    b+=math_text(862,470,"B = [ 1  0   0  −1 ]",26,INK,"middle",700)
    b+=math_text(862,510,"      [ 0  1  −1  −1 ]",26,INK,"middle",700)
    b+=line(635,550,1090,550,GRID,1.5)
    b+=math_text(862,600,"I = BᵀJ = [ J₁  J₂  −J₂  −J₁−J₂ ]ᵀ",20,PURPLE,"middle",700)
    save("fig-04-tree-tieset.svg",b,w,h,"Tree links และ tie-set matrix")


def fig05() -> None:
    w,h=1200,790
    b=title_block("Branch Cards ก่อนคูณเมทริกซ์", "ทุกแถวของ V=ZI+Vₛ−ZIₛ มองเห็นได้จากการ์ด",w)
    cards=[(55,150,"กิ่ง 1 · Thévenin",["Z₁=R₁","Vsb,1=+V₀","V₁=R₁I₁+V₀"],RED,"#fef2f2"),
           (335,150,"กิ่ง 2 · Norton",["Z₂=R₂","Isb,2=+jI₀","V₂=R₂(I₂−jI₀)"],BLUE,"#eff6ff"),
           (615,150,"กิ่ง 3 · Capacitor",["Z₃=−jXC","ไม่มี source","V₃=ZCI₃"],GREEN,"#ecfdf5"),
           (895,150,"กิ่ง 4 · Inductor",["Z₄=+jXL","ไม่มี source","V₄=ZLI₄"],AMBER,"#fff7ed")]
    for x,y,title_,vals,color,fill in cards:
        b+=rect(x,y,250,235,fill,color,18,1.7)+pill(x+20,y+20,170,title_,color)+lines(x+24,y+100,vals,17,INK,"start",38,600,MATH)
    b+=arrow(600,405,600,455,CYAN,4)
    b+=rect(95,470,1010,250,SOFT,GRID,20)
    b+=pill(125,495,170,"VECTOR ASSEMBLY",PURPLE)
    b+=math_text(600,565,"Zᵦ = diag(R₁, R₂, ZC, ZL)",24,INK,"middle",700)
    b+=math_text(600,615,"Vₛᵦ = [ V₀  0  0  0 ]ᵀ     Iₛᵦ = [ 0  jI₀  0  0 ]ᵀ",21,INK,"middle",600)
    b+=math_text(600,675,"Vᵦ = [ R₁I₁+V₀,  R₂(I₂−jI₀),  ZCI₃,  ZLI₄ ]ᵀ",22,PURPLE,"middle",700)
    b+=text(600,760,"เครื่องหมาย +jI₀ เกิดจาก sine phase และการกลับทิศลูกศรอย่างละหนึ่งครั้ง",16,MUTED,"middle",600)
    save("fig-05-branch-models.svg",b,w,h,"แบบจำลองกิ่งและเวกเตอร์กิ่ง")


def fig06() -> None:
    w,h=1200,850
    b=title_block("Complex Matrix Engine", "คูณสามก้อนและเห็นที่มาของทุกสัมประสิทธิ์",w)
    b+=rect(50,135,1100,185,SOFT,GRID)
    blocks=[(75,"1  LOOP MATRIX","BZᵦBᵀ","[R₁+ZL   ZL;  ZL   R₂+ZC+ZL]",BLUE),
            (420,"2  NORTON","BZᵦIₛᵦ","[ 0;  jR₂I₀ ]",PURPLE),
            (790,"3  THÉVENIN","−BVₛᵦ","[ −V₀;  0 ]",AMBER)]
    for x,label,formula,result,color in blocks:
        b+=pill(x,158,150,label,color)+math_text(x+145,235,formula,21,INK,"middle",600)+math_text(x+145,282,result,18,color,"middle",700)
    b+=arrow(600,335,600,390,CYAN,4)
    b+=rect(105,405,990,280,"#eff6ff",BLUE,22,2)+pill(140,435,185,"LOOP SYSTEM 2×2",BLUE)
    b+=math_text(600,525,"[ R₁+ZL       ZL       ] [ J₁ ]   =   [ −V₀      ]",27,INK,"middle",700)
    b+=math_text(600,575,"[   ZL    R₂+ZC+ZL ] [ J₂ ]       [ jR₂I₀ ]",27,INK,"middle",700)
    b+=line(155,615,1045,615,GRID,1.5)
    b+=math_text(600,657,"Δ=(R₁+ZL)(R₂+ZC+ZL)−ZL²",24,RED,"middle",800)
    b+=rect(115,725,970,78,"#ecfdf5",GREEN,15,1.5)
    b+=math_text(600,760,"Δ = [R₁R₂+L/C] + j[ωL(R₁+R₂)−R₁/(ωC)]",21,GREEN,"middle",700)
    b+=text(600,789,"Re{Δ}>0 เมื่อ R₁,R₂,L,C>0  ⇒  ระบบมีคำตอบเอกลักษณ์",15,MUTED,"middle",600)
    save("fig-06-matrix-engine.svg",b,w,h,"การคูณเมทริกซ์วงรอบเชิงซ้อน")


def fig07() -> None:
    w,h=1200,850
    b=title_block("แผนที่คำตอบเชิงสัญลักษณ์", "Iₖ=Nₖ/Δ แล้วแปลง rectangular → polar → time",w)
    b+=rect(410,135,380,110,"#fff7ed",AMBER,18,2)+math_text(600,180,"Δ=Δᵣ+jΔᵢ",28,AMBER,"middle",800)+math_text(600,220,"θΔ=atan2(Δᵢ,Δᵣ)",17,MUTED,"middle",600)
    cards=[(55,300,"N₁ / I₁",["R₂(XL I₀−V₀)","+ jV₀(XC−XL)"],RED),
           (345,300,"N₂ / I₂",["−XL R₂I₀","+ j(XL V₀+R₁R₂I₀)"],BLUE),
           (635,300,"N₃ / I₃",["−N₂","I₃=−I₂"],GREEN),
           (925,300,"N₄ / I₄",["R₂V₀","− j(V₀XC+R₁R₂I₀)"],PURPLE)]
    for x,y,title_,vals,color in cards:
        b+=rect(x,y,220,190,SOFT,color,17,1.7)+pill(x+20,y+20,115,title_,color)+lines(x+20,y+105,vals,15,INK,"start",33,600,MATH)
    b+=arrow(600,515,600,565,CYAN,4)
    b+=rect(115,580,970,170,"#eff6ff",BLUE,18,1.7)
    b+=math_text(600,625,"Aₖ = √(Nₖᵣ²+Nₖᵢ²) / √(Δᵣ²+Δᵢ²)",23,INK,"middle",700)
    b+=math_text(600,675,"φₖ = atan2(Nₖᵢ,Nₖᵣ) − atan2(Δᵢ,Δᵣ)",22,PURPLE,"middle",700)
    b+=math_text(600,724,"iₖ(t)=Aₖ cos(ωt+φₖ)",27,BLUE,"middle",800)
    b+=text(600,805,"กิ่ง 3: A₃=A₂ และ φ₃=wrap(φ₂+180°)",17,MUTED,"middle",650)
    save("fig-07-symbolic-map.svg",b,w,h,"แผนที่คำตอบกระแสเชิงสัญลักษณ์และเวลา")


def fig08() -> None:
    w,h=1200,850
    b=title_block("Numerical Check และ Complex Power", "R₁=4Ω, R₂=6Ω, L=.1H, C=.05F, ω=10, V₀=8V, I₀=1.5A",w)
    b+=rect(55,140,520,285,SOFT,GRID)+pill(85,168,150,"BRANCH CURRENTS",BLUE)
    vals=["I₁=1.5267∠164.01° A","I₂=1.7223∠97.16° A","I₃=1.7223∠−82.84° A","I₄=2.7138∠−51.69° A"]
    b+=lines(90,245,vals,18,INK,"start",42,600,MATH)
    b+=rect(625,140,520,285,"#ecfdf5",GREEN)+pill(655,168,135,"KVL + KCL",GREEN)
    b+=math_text(885,250,"V₁−V₄ = 0",23,INK,"middle",700)
    b+=math_text(885,300,"V₂−V₃−V₄ = 0",23,INK,"middle",700)
    b+=math_text(885,350,"I₂+I₃ = 0",23,INK,"middle",700)
    b+=math_text(885,395,"I₁+I₄−I₃ = 0",23,GREEN,"middle",800)
    b+=rect(55,465,1090,300,PAPER,GRID)+pill(85,493,175,"COMPLEX POWER",PURPLE)
    powers=[("R₁","+4.662+j0",GREEN),("Vₛ","−5.871−j1.682",RED),("R₂","+.269+j0",GREEN),
            ("Iₛ","+.940+j.966",AMBER),("C","−j2.966",BLUE),("L","+j3.682",PURPLE)]
    x=80
    for label,value,color in powers:
        b+=rect(x,560,160,120,SOFT,color,13,1.5)+pill(x+20,578,75,label,color)+math_text(x+80,648,value,16,INK,"middle",700)
        x+=175
    b+=rect(325,705,550,43,"#ecfdf5",GREEN,12,1.5)+math_text(600,733,"ΣS = 0 + j0 VA  ✓",22,GREEN,"middle",800)
    b+=text(600,820,"ใช้ peak phasor: S=(1/2)VI*",17,MUTED,"middle",650)
    save("fig-08-numeric-check.svg",b,w,h,"ตัวอย่างตัวเลข KVL KCL และสมดุลกำลังเชิงซ้อน")


def main() -> None:
    for fn in (fig01,fig02,fig03,fig04,fig05,fig06,fig07,fig08):
        fn()
    print(f"Generated 8 SVG files in {OUT}")


if __name__ == "__main__":
    main()
