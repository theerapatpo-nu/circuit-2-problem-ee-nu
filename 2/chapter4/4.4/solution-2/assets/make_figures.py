#!/usr/bin/env python3
"""Generate the exam-oriented vector diagrams for problem 4.4, solution 2.

The SVGs use fixed viewBox coordinates, straight geometry, large labels, and no
external Python dependencies. Run this file from any working directory.
"""

from pathlib import Path


OUT = Path(__file__).resolve().parent


def save(name: str, body: str, title: str, desc: str, height: int = 720) -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}"
  role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <defs>
    <marker id="arrowBlue" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto">
      <path d="M0,0 L18,9 L0,18 Z" fill="#2563eb"/>
    </marker>
    <marker id="arrowRed" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto">
      <path d="M0,0 L18,9 L0,18 Z" fill="#dc2626"/>
    </marker>
    <marker id="arrowDark" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto">
      <path d="M0,0 L18,9 L0,18 Z" fill="#172033"/>
    </marker>
    <filter id="shadow" x="-15%" y="-15%" width="130%" height="140%">
      <feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#0f172a" flood-opacity=".12"/>
    </filter>
    <style>
      .bg {{ fill:#f8fafc; }} .paper {{ fill:#fff; stroke:#dbe3ee; stroke-width:2; }}
      .title {{ font:700 31px 'Noto Sans Thai','Sarabun','Segoe UI',sans-serif; fill:#0f172a; }}
      .head {{ font:700 24px 'Noto Sans Thai','Sarabun','Segoe UI',sans-serif; fill:#172033; }}
      .body {{ font:500 20px 'Noto Sans Thai','Sarabun','Segoe UI',sans-serif; fill:#334155; }}
      .small {{ font:500 17px 'Noto Sans Thai','Sarabun','Segoe UI',sans-serif; fill:#64748b; }}
      .math {{ font:italic 25px Georgia,'Times New Roman',serif; fill:#172033; }}
      .mathBig {{ font:italic 32px Georgia,'Times New Roman',serif; font-weight:700; fill:#172033; }}
      .chip {{ font:700 19px 'Noto Sans Thai','Sarabun','Segoe UI',sans-serif; }}
      .wire {{ fill:none; stroke:#172033; stroke-width:7; stroke-linecap:round; stroke-linejoin:round; }}
      .tree {{ fill:none; stroke:#172033; stroke-width:11; stroke-linecap:round; }}
      .link {{ fill:none; stroke:#dc2626; stroke-width:8; stroke-linecap:round; }}
      .guide {{ fill:none; stroke:#94a3b8; stroke-width:2; stroke-dasharray:7 7; }}
    </style>
  </defs>
  <rect class="bg" width="1200" height="{height}" rx="28"/>
{body}
</svg>'''
    (OUT / name).write_text(svg, encoding="utf-8")


def figure_01() -> None:
    body = '''
  <text class="title" x="60" y="65">แผนทำข้อสอบ: รูปนำทาง สมการตามมา</text>
  <text class="small" x="60" y="100">ใช้ภาพหนึ่งรูปกำหนดทิศทั้งหมด แล้วกรอกเมทริกซ์เพียงหนึ่งแถว</text>
  <g filter="url(#shadow)">
    <rect class="paper" x="55" y="145" width="245" height="390" rx="24"/>
    <rect x="55" y="145" width="245" height="68" rx="24" fill="#dbeafe"/>
    <text class="head" x="178" y="188" text-anchor="middle">1 · วงทรี</text>
    <circle cx="178" cy="300" r="61" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>
    <path d="M141 324 A52 52 0 1 1 218 323" fill="none" stroke="#2563eb" stroke-width="6" marker-end="url(#arrowBlue)"/>
    <text class="mathBig" x="178" y="309" text-anchor="middle">j₁</text>
    <text class="body" x="178" y="411" text-anchor="middle">เดินตามลูกศรลิงก์ 1</text>
    <text class="small" x="178" y="447" text-anchor="middle">O → B → A → O</text>
    <text class="chip" x="178" y="498" text-anchor="middle" fill="#2563eb">ทิศเดียว = +</text>

    <rect class="paper" x="335" y="145" width="245" height="390" rx="24"/>
    <rect x="335" y="145" width="245" height="68" rx="24" fill="#fee2e2"/>
    <text class="head" x="458" y="188" text-anchor="middle">2 · อ่านเครื่องหมาย</text>
    <rect x="373" y="260" width="170" height="65" rx="15" fill="#ecfdf5"/>
    <text class="mathBig" x="458" y="304" text-anchor="middle">+1</text>
    <rect x="373" y="344" width="170" height="65" rx="15" fill="#ecfdf5"/>
    <text class="mathBig" x="458" y="388" text-anchor="middle">+1</text>
    <rect x="373" y="428" width="170" height="65" rx="15" fill="#fff1f2"/>
    <text class="mathBig" x="458" y="472" text-anchor="middle" fill="#dc2626">−1</text>

    <rect class="paper" x="615" y="145" width="245" height="390" rx="24"/>
    <rect x="615" y="145" width="245" height="68" rx="24" fill="#ede9fe"/>
    <text class="head" x="738" y="188" text-anchor="middle">3 · กรอกเมทริกซ์</text>
    <text class="small" x="738" y="273" text-anchor="middle">เรียงคอลัมน์ [1, 2, 3]</text>
    <rect x="653" y="307" width="170" height="92" rx="17" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="3"/>
    <text class="mathBig" x="738" y="365" text-anchor="middle">B = [1  1  −1]</text>
    <text class="body" x="738" y="451" text-anchor="middle">หนึ่งลิงก์</text>
    <text class="chip" x="738" y="490" text-anchor="middle" fill="#7c3aed">⇒ หนึ่งแถว</text>

    <rect class="paper" x="895" y="145" width="250" height="390" rx="24"/>
    <rect x="895" y="145" width="250" height="68" rx="24" fill="#fef3c7"/>
    <text class="head" x="1020" y="188" text-anchor="middle">4 · คูณ 3 ก้อน</text>
    <text class="math" x="1020" y="284" text-anchor="middle">BZBᵀ</text>
    <text class="chip" x="1020" y="322" text-anchor="middle" fill="#b45309">ความต้านทานรอบ</text>
    <text class="math" x="1020" y="388" text-anchor="middle">BZ iₛ</text>
    <text class="chip" x="1020" y="426" text-anchor="middle" fill="#b45309">แรงขับ Norton</text>
    <text class="math" x="1020" y="492" text-anchor="middle">−B vₛ</text>
  </g>
  <path d="M300 340 H326" stroke="#94a3b8" stroke-width="4" marker-end="url(#arrowDark)"/>
  <path d="M580 340 H606" stroke="#94a3b8" stroke-width="4" marker-end="url(#arrowDark)"/>
  <path d="M860 340 H886" stroke="#94a3b8" stroke-width="4" marker-end="url(#arrowDark)"/>
  <rect x="190" y="585" width="820" height="78" rx="18" fill="#0f172a"/>
  <text x="600" y="635" text-anchor="middle" font-family="Georgia,serif" font-size="28" font-style="italic" fill="#fff">Rₜ j₁ = (R₂ + R₃)iₛ − vₛ</text>
'''
    save("fig-01-exam-roadmap.svg", body, "แผนทำข้อสอบแบบ Visual Matrix", "สี่ขั้นจากวงทรีถึงสมการวงรอบ")


def figure_02() -> None:
    body = '''
  <text class="title" x="60" y="65">อ่าน B จากรูปทรี: ตาม ตาม สวน</text>
  <text class="small" x="60" y="100">ลำดับคอลัมน์ต้องตรงกับเวกเตอร์กิ่ง [1, 2, 3] เสมอ</text>
  <g transform="translate(60 130)" filter="url(#shadow)">
    <rect class="paper" x="0" y="0" width="700" height="500" rx="24"/>
    <circle cx="120" cy="120" r="13" fill="#172033"/>
    <circle cx="580" cy="120" r="13" fill="#dc2626"/>
    <circle cx="350" cy="405" r="13" fill="#dc2626"/>
    <text class="head" x="85" y="102">A</text>
    <text class="head" x="602" y="102">B</text>
    <text class="head" x="367" y="443">O</text>
    <path class="tree" d="M568 120 H139"/>
    <path class="tree" d="M342 394 L129 134"/>
    <path class="link" d="M359 394 L571 134"/>
    <path d="M455 120 H335" fill="none" stroke="#172033" stroke-width="7" marker-end="url(#arrowDark)"/>
    <path d="M290 330 L222 247" fill="none" stroke="#172033" stroke-width="7" marker-end="url(#arrowDark)"/>
    <path d="M426 311 L500 220" fill="none" stroke="#dc2626" stroke-width="7" marker-end="url(#arrowRed)"/>
    <text class="mathBig" x="350" y="91">2</text>
    <text class="mathBig" x="205" y="300">3</text>
    <text class="mathBig" x="507" y="300" fill="#dc2626">1</text>
    <path d="M263 299 A118 118 0 1 1 439 298" fill="none" stroke="#2563eb" stroke-width="5" stroke-dasharray="10 8" marker-end="url(#arrowBlue)"/>
    <text class="mathBig" x="350" y="285" text-anchor="middle" fill="#2563eb">j₁</text>
  </g>
  <g transform="translate(805 145)">
    <text class="head" x="0" y="0">ใช้ดินสอวงทีละกิ่ง</text>
    <rect x="0" y="40" width="330" height="80" rx="16" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="2"/>
    <text class="chip" x="25" y="77" fill="#047857">กิ่ง 1</text><text class="body" x="115" y="77">O → B</text>
    <text class="chip" x="285" y="87" fill="#047857">+1</text>
    <rect x="0" y="140" width="330" height="80" rx="16" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="2"/>
    <text class="chip" x="25" y="177" fill="#047857">กิ่ง 2</text><text class="body" x="115" y="177">B → A</text>
    <text class="chip" x="285" y="187" fill="#047857">+1</text>
    <rect x="0" y="240" width="330" height="80" rx="16" fill="#fff1f2" stroke="#fda4af" stroke-width="2"/>
    <text class="chip" x="25" y="277" fill="#be123c">กิ่ง 3</text><text class="body" x="115" y="277">A → O</text>
    <text class="chip" x="285" y="287" fill="#be123c">−1</text>
    <rect x="0" y="350" width="330" height="108" rx="18" fill="#eff6ff" stroke="#60a5fa" stroke-width="3"/>
    <text class="small" x="165" y="385" text-anchor="middle">ผลที่อ่านจากภาพ</text>
    <text class="mathBig" x="165" y="435" text-anchor="middle">B = [1  1  −1]</text>
  </g>
'''
    save("fig-02-read-b-from-tree.svg", body, "อ่านเมทริกซ์ B จากทรี", "แผนภาพทรีสมมาตรและตารางเครื่องหมายของกิ่ง 1 2 3")


def figure_03() -> None:
    body = '''
  <text class="title" x="60" y="65">Matrix workbench: กรอกช่อง แล้วคูณทีละก้อน</text>
  <text class="small" x="60" y="100">เมทริกซ์ทุกตัวเรียงกิ่ง [1, 2, 3] เหมือนกัน จึงลดความผิดพลาดเรื่อง R และเครื่องหมาย</text>
  <g filter="url(#shadow)">
    <rect class="paper" x="55" y="140" width="1090" height="190" rx="24"/>
    <text class="head" x="90" y="185">โต๊ะเตรียม</text>
    <rect x="90" y="215" width="225" height="78" rx="15" fill="#eff6ff"/>
    <text class="math" x="202" y="264" text-anchor="middle">B = [1  1  −1]</text>
    <rect x="335" y="215" width="290" height="78" rx="15" fill="#f5f3ff"/>
    <text class="math" x="480" y="264" text-anchor="middle">Z = diag(R₃,R₂,R₁)</text>
    <rect x="645" y="215" width="210" height="78" rx="15" fill="#ecfdf5"/>
    <text class="math" x="750" y="264" text-anchor="middle">iₛ = [iₛ iₛ 0]ᵀ</text>
    <rect x="875" y="215" width="230" height="78" rx="15" fill="#fff1f2"/>
    <text class="math" x="990" y="264" text-anchor="middle">vₛ = [0 0 −vₛ]ᵀ</text>

    <rect class="paper" x="55" y="365" width="330" height="215" rx="24"/>
    <circle cx="108" cy="418" r="26" fill="#2563eb"/>
    <text x="108" y="427" text-anchor="middle" font-size="24" font-weight="700" fill="#fff">1</text>
    <text class="head" x="150" y="427">ก้อนซ้าย</text>
    <text class="mathBig" x="220" y="490" text-anchor="middle">BZBᵀ = Rₜ</text>
    <text class="small" x="220" y="535" text-anchor="middle">Rₜ = R₁ + R₂ + R₃</text>

    <rect class="paper" x="435" y="365" width="330" height="215" rx="24"/>
    <circle cx="488" cy="418" r="26" fill="#059669"/>
    <text x="488" y="427" text-anchor="middle" font-size="24" font-weight="700" fill="#fff">2</text>
    <text class="head" x="530" y="427">Norton drive</text>
    <text class="mathBig" x="600" y="490" text-anchor="middle">BZ iₛ</text>
    <text class="small" x="600" y="535" text-anchor="middle">= (R₂ + R₃)iₛ</text>

    <rect class="paper" x="815" y="365" width="330" height="215" rx="24"/>
    <circle cx="868" cy="418" r="26" fill="#dc2626"/>
    <text x="868" y="427" text-anchor="middle" font-size="24" font-weight="700" fill="#fff">3</text>
    <text class="head" x="910" y="427">Thévenin drive</text>
    <text class="mathBig" x="980" y="490" text-anchor="middle">−Bvₛ</text>
    <text class="small" x="980" y="535" text-anchor="middle">= −vₛ</text>
  </g>
  <path d="M385 472 H426" stroke="#94a3b8" stroke-width="4" marker-end="url(#arrowDark)"/>
  <path d="M765 472 H806" stroke="#94a3b8" stroke-width="4" marker-end="url(#arrowDark)"/>
  <rect x="235" y="620" width="730" height="74" rx="18" fill="#0f172a"/>
  <text x="600" y="668" text-anchor="middle" font-family="Georgia,serif" font-size="30" font-style="italic" fill="#fff">Rₜj₁ = (R₂ + R₃)iₛ − vₛ</text>
'''
    save("fig-03-matrix-workbench.svg", body, "โต๊ะคำนวณเมทริกซ์", "เมทริกซ์ตั้งต้นและการคูณสามก้อนเพื่อหาสมการวงรอบ")


def figure_04() -> None:
    body = '''
  <text class="title" x="60" y="65">Answer map: จาก j₁ ไปครบทุกคำตอบ</text>
  <text class="small" x="60" y="100">จำความสัมพันธ์จากรูปเพียงสองลูกศร: i = Bᵀj และ v = Zi + vₛ − Ziₛ</text>
  <g filter="url(#shadow)">
    <rect x="385" y="145" width="430" height="105" rx="22" fill="#0f172a"/>
    <text x="600" y="189" text-anchor="middle" font-family="Georgia,serif" font-size="25" font-style="italic" fill="#cbd5e1">loop current</text>
    <text x="600" y="228" text-anchor="middle" font-family="Georgia,serif" font-size="29" font-style="italic" fill="#fff">j₁ = ((R₂+R₃)iₛ−vₛ)/Rₜ</text>

    <rect class="paper" x="55" y="365" width="500" height="245" rx="24"/>
    <rect x="55" y="365" width="500" height="62" rx="24" fill="#dbeafe"/>
    <text class="head" x="305" y="405" text-anchor="middle">กระแสกิ่ง: อ่านจากคอลัมน์ Bᵀ</text>
    <text class="mathBig" x="305" y="485" text-anchor="middle">i₁ = j₁</text>
    <text class="mathBig" x="305" y="535" text-anchor="middle">i₂ = j₁</text>
    <text class="mathBig" x="305" y="585" text-anchor="middle">i₃ = −j₁</text>

    <rect class="paper" x="645" y="365" width="500" height="245" rx="24"/>
    <rect x="645" y="365" width="500" height="62" rx="24" fill="#dcfce7"/>
    <text class="head" x="895" y="405" text-anchor="middle">แรงดันกิ่ง: แทนใน branch cards</text>
    <text class="math" x="895" y="482" text-anchor="middle">v₁ = R₃(i₁−iₛ)</text>
    <text class="math" x="895" y="532" text-anchor="middle">v₂ = R₂(i₂−iₛ)</text>
    <text class="math" x="895" y="582" text-anchor="middle">v₃ = R₁i₃−vₛ</text>
  </g>
  <path d="M520 250 C460 290 370 310 310 355" fill="none" stroke="#2563eb" stroke-width="5" marker-end="url(#arrowBlue)"/>
  <path d="M680 250 C740 290 830 310 890 355" fill="none" stroke="#059669" stroke-width="5" marker-end="url(#arrowDark)"/>
  <rect x="195" y="648" width="810" height="50" rx="14" fill="#fff7ed" stroke="#fdba74" stroke-width="2"/>
  <text class="chip" x="600" y="681" text-anchor="middle" fill="#b45309">ตรวจปลายทาง:  i₁ = i₂ = −i₃   และ   v₁ + v₂ − v₃ = 0</text>
'''
    save("fig-04-answer-map.svg", body, "แผนที่คำตอบจากกระแสวงรอบ", "แตกกระแสวงรอบเป็นกระแสกิ่งและแรงดันกิ่ง พร้อมเงื่อนไขตรวจคำตอบ")


def main() -> None:
    figure_01()
    figure_02()
    figure_03()
    figure_04()
    print("Generated 4 SVG files in", OUT)


if __name__ == "__main__":
    main()
