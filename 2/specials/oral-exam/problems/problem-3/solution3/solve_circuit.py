#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solve_circuit.py — เฉลยโจทย์สอบปากเปล่า 303212 ข้อที่ 3 ฉบับตรวจสอบได้ทุกตัวเลข
===============================================================================

โจทย์: วงข่ายความนำไฟฟ้า G1..G4 กับแหล่งจ่ายแรงดันอิสระ E1, E2, E3
       จงเขียนสมการชุดตัดในรูปเมทริกซ์เวกเตอร์ และหา Va, Vb, Vc, Vd
       (ดู ../oral_exam_problem.md และ ../circuit_fig3.png)

โครงสร้างวงจร (5 ปม a,b,c,d,e และ 7 กิ่ง):
    E1 : a-e   ขั้ว + ที่ a   ->  Va = +E1
    G1 : a-b
    G3 : b-e
    E3 : b-c   ขั้ว + ที่ c   ->  Vc - Vb = +E3
    G2 : c-d
    G4 : d-e
    E2 : d-e   ขั้ว - ที่ d   ->  Vd = -E2      <-- กับดักเครื่องหมาย!

สคริปต์นี้ทำ 6 อย่าง เรียงตามลำดับที่ควรอธิบายในห้องสอบ:

    ขั้นที่ 1  สร้างกราฟวงจรและเมทริกซ์อุบัติการณ์ [A]
    ขั้นที่ 2  เลือกต้นไม้ (ยัดแหล่งจ่ายเข้าเป็นกิ่งต้นไม้) และตรวจว่าเป็นต้นไม้จริง
    ขั้นที่ 3  สร้างเมทริกซ์ชุดตัดพื้นฐาน [Q_K] และเมทริกซ์ลูป [B] + ตรวจ Q B^T = 0
    ขั้นที่ 4  คำนวณ [Q_G][Y_b][Q_G]^T และดึงสมการ supernode ออกมา
    ขั้นที่ 5  แก้หาแรงดันปม 3 เส้นทางที่เป็นอิสระกัน แล้วเทียบผล
    ขั้นที่ 6  ตรวจ KCL, สมดุลกำลังไฟฟ้า และทดสอบว่า G4 ไม่มีผลต่อแรงดัน

ต้องการแค่ NumPy เท่านั้น

วิธีรัน:
    python3 solve_circuit.py
    python3 solve_circuit.py --G1 0.5 --G2 0.25 --G3 0.2 --G4 0.4 --E1 12 --E2 6 --E3 4
    python3 solve_circuit.py --json out.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

SEP = "=" * 78
SUB = "-" * 78
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# นิยามกราฟวงจร
# ---------------------------------------------------------------------------
# เรียงกิ่งแบบ "กิ่งต้นไม้ก่อน แล้วค่อยกิ่งร่วม" เพื่อให้ [Q] ออกมาในรูป [I | Ql]
BRANCHES = ["E1", "G3", "E3", "E2", "G1", "G2", "G4"]
TWIGS = ["E1", "G3", "E3", "E2"]        # ต้นไม้ที่เลือก
LINKS = ["G1", "G2", "G4"]              # กิ่งร่วม
NODES = ["a", "b", "c", "d", "e"]
REF = "e"                                # ปมอ้างอิง (กราวด์)

# ทิศทางอ้างอิงของแต่ละกิ่ง: (from, to) และ v_branch = V(from) - V(to)
ORIENT = {
    "E1": ("a", "e"),
    "G3": ("b", "e"),
    "E3": ("c", "b"),
    "E2": ("d", "e"),
    "G1": ("a", "b"),
    "G2": ("c", "d"),
    "G4": ("d", "e"),
}


def head(title: str) -> None:
    print("\n" + SEP)
    print(title)
    print(SEP)


def build_incidence():
    """สร้างเมทริกซ์อุบัติการณ์สมบูรณ์ Aa (5x7) และแบบลดรูป A (4x7)"""
    idx = {n: i for i, n in enumerate(NODES)}
    Aa = np.zeros((len(NODES), len(BRANCHES)))
    for j, b in enumerate(BRANCHES):
        f, t = ORIENT[b]
        Aa[idx[f], j] += 1.0
        Aa[idx[t], j] -= 1.0
    A = np.delete(Aa, idx[REF], axis=0)   # ตัดแถวของปมอ้างอิงออก
    return Aa, A


def build_cutset(A):
    """สร้าง [Q_K] = [I | Ql] โดยใช้ Ql = At^{-1} Al"""
    nt = len(TWIGS)
    At, Al = A[:, :nt], A[:, nt:]
    det = float(np.linalg.det(At))
    Ql = np.linalg.solve(At, Al)
    Q = np.hstack([np.eye(nt), Ql])
    B = np.hstack([-Ql.T, np.eye(len(LINKS))])   # เมทริกซ์ลูปพื้นฐาน
    return Q, B, Ql, det


def show_matrix(M, rows, cols, title, fmt="{:>7.3g}"):
    print(f"\n{title}")
    print("        " + "".join(f"{c:>8}" for c in cols))
    for i, r in enumerate(rows):
        print(f"  {r:>5} " + "".join(fmt.format(M[i, j]) for j in range(M.shape[1])))


# ---------------------------------------------------------------------------
# สามเส้นทางแก้ปัญหาที่เป็นอิสระจากกัน
# ---------------------------------------------------------------------------
def route_A_closed_form(G1, G2, G3, G4, E1, E2, E3):
    """เส้นทาง A: สูตรปิดที่พิสูจน์ด้วยมือในบทที่ 2"""
    den = G1 + G2 + G3
    Vb = (G1 * E1 - G2 * E2 - G2 * E3) / den
    Vc = (G1 * E1 - G2 * E2 + (G1 + G3) * E3) / den
    return np.array([E1, Vb, Vc, -E2])


def route_B_cutset(QG, G1, G2, G3, G4, E1, E2, E3):
    """เส้นทาง B: สมการชุดตัด [Q_G][Y_b][Q_G]^T แถวที่ 2 (ดัชนี 1)

    เวกเตอร์แรงดันกิ่งต้นไม้ v_t = [Va, Vb, Vc-Vb, Vd] = [E1, Vb, E3, -E2]
    แถวที่ 2 เป็นแถวเดียวที่ไม่มีแหล่งจ่ายพาดผ่าน ฝั่งขวาจึงเป็นศูนย์แท้ๆ
    """
    Yb = np.diag([G3, G1, G2, G4])          # เรียงตาม [G3, G1, G2, G4]
    M = QG @ Yb @ QG.T
    row = M[1]
    # row . [E1, Vb, E3, -E2] = 0  ->  แก้หา Vb
    Vb = -(row[0] * E1 + row[2] * E3 + row[3] * (-E2)) / row[1]
    return np.array([E1, Vb, Vb + E3, -E2]), M


def route_C_linear_system(G1, G2, G3, G4, E1, E2, E3):
    """เส้นทาง C: ตั้งระบบ A x = b แล้วให้ numpy แก้ (x = [Va,Vb,Vc,Vd])"""
    A = np.array([
        [1.0,  0.0,      0.0,  0.0],      # Va = E1
        [0.0,  0.0,      0.0,  1.0],      # Vd = -E2
        [0.0, -1.0,      1.0,  0.0],      # Vc - Vb = E3
        [-G1,  G1 + G3,  G2,  -G2],       # KCL ที่ supernode (b,c)
    ])
    b = np.array([E1, -E2, E3, 0.0])
    return np.linalg.solve(A, b), A, b


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--G1", type=float, default=0.5, help="ความนำกิ่ง a-b [mho]")
    ap.add_argument("--G2", type=float, default=0.25, help="ความนำกิ่ง c-d [mho]")
    ap.add_argument("--G3", type=float, default=0.2, help="ความนำกิ่ง b-e [mho]")
    ap.add_argument("--G4", type=float, default=0.4, help="ความนำกิ่ง d-e [mho]")
    ap.add_argument("--E1", type=float, default=12.0, help="แหล่งจ่าย a-e, + ที่ a [V]")
    ap.add_argument("--E2", type=float, default=6.0, help="แหล่งจ่าย d-e, - ที่ d [V]")
    ap.add_argument("--E3", type=float, default=4.0, help="แหล่งจ่าย b-c, + ที่ c [V]")
    ap.add_argument("--json", nargs="?", const="results.json",
                    help="บันทึกผลลัพธ์เป็นไฟล์ JSON")
    ap.add_argument("--trials", type=int, default=500,
                    help="จำนวนชุดสุ่มสำหรับตรวจไขว้ (0 = ข้าม)")
    a = ap.parse_args()
    G1, G2, G3, G4 = a.G1, a.G2, a.G3, a.G4
    E1, E2, E3 = a.E1, a.E2, a.E3

    print(SEP)
    print("เฉลยโจทย์สอบปากเปล่า 303212 ข้อที่ 3 — วงข่ายความนำไฟฟ้าและสมการชุดตัด")
    print("problems/problem-3/solution3/solve_circuit.py")
    print(SEP)
    print(f"\nพารามิเตอร์: G1={G1} G2={G2} G3={G3} G4={G4} [mho]"
          f"   E1={E1} E2={E2} E3={E3} [V]")
    print(f"ความต้านทานเทียบเท่า: R1={1/G1:.6g} R2={1/G2:.6g} "
          f"R3={1/G3:.6g} R4={1/G4:.6g} [ohm]")

    # ---------------- ขั้นที่ 1 ----------------
    head("ขั้นที่ 1 — กราฟวงจรและเมทริกซ์อุบัติการณ์ [A]")
    n, b = len(NODES), len(BRANCHES)
    print(f"\n  จำนวนปม n = {n}  ({', '.join(NODES)})   ปมอ้างอิง = {REF}")
    print(f"  จำนวนกิ่ง b = {b}  ({', '.join(BRANCHES)})   <-- นับแหล่งจ่ายเป็นกิ่งด้วย!")
    print(f"  กิ่งต้นไม้ = n - 1 = {n-1}   กิ่งร่วม = b - n + 1 = {b-n+1}")

    Aa, A = build_incidence()
    show_matrix(Aa, NODES, BRANCHES, "เมทริกซ์อุบัติการณ์สมบูรณ์ [Aa] (5x7):")
    csum = Aa.sum(axis=0)
    print(f"\n  ผลรวมแต่ละคอลัมน์ = {csum}")
    print(f"  เป็นศูนย์ทุกคอลัมน์? {np.allclose(csum, 0)}"
          "   <- ทุกกิ่งมี 2 ปลาย ปลายหนึ่ง +1 อีกปลาย -1")
    show_matrix(A, [x for x in NODES if x != REF], BRANCHES,
                "เมทริกซ์อุบัติการณ์ลดรูป [A] (4x7) — ตัดแถวปมอ้างอิงออก:")

    # ---------------- ขั้นที่ 2 ----------------
    head("ขั้นที่ 2 — เลือกต้นไม้ และตรวจว่าเป็นต้นไม้จริง")
    print(f"\n  ต้นไม้ที่เลือก : {TWIGS}")
    print(f"  กิ่งร่วม        : {LINKS}")
    print("\n  หลักการเลือก: 'ยัดแหล่งจ่ายแรงดันทุกตัวเข้าเป็นกิ่งต้นไม้ให้หมด'")
    print("    เพราะแรงดันกิ่งต้นไม้คือตัวแปรของระบบ")
    print("    ถ้ากิ่งนั้นเป็นแหล่งจ่าย เราก็รู้ค่าตัวแปรฟรีทันที")

    Q, B, Ql, det = build_cutset(A)
    print(f"\n  det[At] = {det:.6g}  -> {'เป็นต้นไม้จริง' if abs(det) > 1e-12 else 'ไม่ใช่ต้นไม้!'}")

    print("\n  แรงดันกิ่งต้นไม้ (ตัวแปรของระบบ):")
    print(f"    v(E1) = Va - Ve = Va       = E1  = {E1}      [รู้ค่า]")
    print(f"    v(G3) = Vb - Ve = Vb       = ?                [<<< ตัวไม่รู้ตัวเดียว]")
    print(f"    v(E3) = Vc - Vb            = E3  = {E3}       [รู้ค่า]")
    print(f"    v(E2) = Vd - Ve = Vd       = -E2 = {-E2}      [รู้ค่า]")
    print(f"\n  => ตัวไม่รู้ที่แท้จริง = (n-1) - (จำนวนแหล่งจ่าย) = {n-1} - 3 = 1 ตัว")

    # ---------------- ขั้นที่ 3 ----------------
    head("ขั้นที่ 3 — เมทริกซ์ชุดตัดพื้นฐาน [Q_K] และเมทริกซ์ลูป [B]")
    cutnames = [f"cut{i+1}({t})" for i, t in enumerate(TWIGS)]
    show_matrix(Q, cutnames, BRANCHES, "[Q_K] = [ I | Ql ]  (4x7):", fmt="{:>7.0f}")
    left_is_I = np.allclose(Q[:, :4], np.eye(4))
    print(f"\n  บล็อกซ้าย (กิ่งต้นไม้) เป็นเมทริกซ์เอกลักษณ์ I4? {left_is_I}"
          "   <- ต้องเป็นเสมอ ถ้าไม่ใช่แสดงว่าทำผิด")

    print("\n  อ่านแถวที่ 2 (รอยตัดของกิ่ง G3) ให้เป็น:")
    print("    ตัด G3 ออก -> กราฟขาดเป็น {b, c} กับ {a, d, e}")
    print("    (b กับ c ยังเชื่อมกันด้วย E3 จึงอยู่ก้อนเดียวกัน)")
    for j, br in enumerate(BRANCHES):
        v = Q[1, j]
        if abs(v) > 1e-9:
            print(f"      {br:>3}: {v:+.0f}  ข้ามรอยตัด")
        elif br == "E3":
            print(f"      {br:>3}:  0   ปลายทั้งสองอยู่ใน {{b,c}} -> ไม่ข้าม  *** นี่คือ supernode! ***")

    show_matrix(B, [f"loop{i+1}({l})" for i, l in enumerate(LINKS)], BRANCHES,
                "[B] = [ -Ql^T | I ]  (3x7):", fmt="{:>7.0f}")
    QBt = Q @ B.T
    print(f"\n  [Q_K][B]^T =\n{np.round(QBt, 12)}")
    print(f"  ตั้งฉากกัน (Q B^T = 0)? {np.allclose(QBt, 0)}"
          "   <- KCL ตั้งฉาก KVL (รากฐานทฤษฎีบทเทลเลเจน)")

    # ---------------- ขั้นที่ 4 ----------------
    head("ขั้นที่ 4 — เมทริกซ์ [Q_G][Y_b][Q_G]^T")
    print("\n  แหล่งจ่ายแรงดันอุดมคติไม่มีค่าความนำ (G -> infinity)")
    print("  จึงเขียน [Y_b] ครบ 7 กิ่งไม่ได้ ต้องหั่นเฉพาะคอลัมน์ของกิ่งความนำ")
    gorder = ["G3", "G1", "G2", "G4"]
    gcols = [BRANCHES.index(x) for x in gorder]
    QG = Q[:, gcols]
    show_matrix(QG, cutnames, gorder, "[Q_G] (4x4):", fmt="{:>7.0f}")
    print(f"\n  [Y_b] = diag({', '.join(gorder)}) = diag({G3}, {G1}, {G2}, {G4})")

    volts, M = route_B_cutset(QG, G1, G2, G3, G4, E1, E2, E3)
    show_matrix(M, cutnames, cutnames, "[Q_G][Y_b][Q_G]^T (4x4):", fmt="{:>9.4f}")
    print(f"\n  สมมาตร? {np.allclose(M, M.T)}   <- ต้องเป็นเสมอ (reciprocal network)")
    print("\n  รูปเชิงสัญลักษณ์:")
    print("      [   G1        -G1          0        0    ]")
    print("      [  -G1    G1+G2+G3        G2      -G2    ]")
    print("      [    0         G2         G2      -G2    ]")
    print("      [    0        -G2        -G2   G2+G4     ]")
    print(f"\n  G4 ปรากฏที่ตำแหน่ง (4,4) ตำแหน่งเดียว = {M[3,3]:.4f}")
    print("    ซึ่งเป็นแถวของรอยตัดที่ตัดผ่าน E2 -> แถวนั้นใช้หากระแสของ E2 เท่านั้น")
    print("    แถวที่ 2 (ที่ใช้แก้หา Vb) ไม่มี G4 เลย -> Vb ไม่ขึ้นกับ G4")

    row = M[1]
    print(f"\n  กางแถวที่ 2 ออกมา (แถวเดียวที่ฝั่งขวาเป็นศูนย์แท้ๆ):")
    print(f"    ({row[0]:+.4f})Va + ({row[1]:+.4f})Vb + ({row[2]:+.4f})(Vc-Vb) "
          f"+ ({row[3]:+.4f})Vd = 0")
    print("    ซึ่งจัดรูปได้เป็น  G1(Vb-Va) + G3*Vb + G2(Vc-Vd) = 0")
    print("    *** นี่คือสมการ KCL ที่ supernode (b,c) เป๊ะ ***")

    # ---------------- ขั้นที่ 5 ----------------
    head("ขั้นที่ 5 — แก้หาแรงดันปม 3 เส้นทางที่เป็นอิสระกัน")
    vA = route_A_closed_form(G1, G2, G3, G4, E1, E2, E3)
    vB = volts
    vC, Amat, bvec = route_C_linear_system(G1, G2, G3, G4, E1, E2, E3)

    print("\n  ระบบสมการเชิงเส้น A x = b ของเส้นทาง C:")
    labels = ["Va = E1", "Vd = -E2", "Vc - Vb = E3", "KCL supernode"]
    print("          " + "".join(f"{c:>10}" for c in ["Va", "Vb", "Vc", "Vd"]) + f"{'|':>4}{'b':>10}")
    for i in range(4):
        print("   " + "".join(f"{Amat[i,j]:>10.4f}" for j in range(4))
              + f"{'|':>4}{bvec[i]:>10.4f}   ({labels[i]})")

    print(f"\n  {'':<26}{'Va':>16}{'Vb':>16}{'Vc':>16}{'Vd':>16}")
    print("  " + SUB)
    for name, v in (("A: สูตรปิด (มือ)", vA),
                    ("B: สมการชุดตัด", vB),
                    ("C: แก้ระบบ Ax=b", vC)):
        print(f"  {name:<24}" + "".join(f"{x:>16.12f}" for x in v))
    agree = np.allclose(vA, vB) and np.allclose(vA, vC)
    print(f"\n  ทั้งสามเส้นทางตรงกัน? {agree}"
          f"   (ต่างกันสูงสุด {max(np.abs(vA-vB).max(), np.abs(vA-vC).max()):.3e})")

    Va, Vb, Vc, Vd = vA
    print(f"\n  === คำตอบ ===")
    print(f"    Va = {Va:.6f} V   (= E1 ; ขั้วบวกอยู่ที่ปม a)")
    print(f"    Vb = {Vb:.6f} V   (จากสมการ supernode)")
    print(f"    Vc = {Vc:.6f} V   (= Vb + E3)")
    print(f"    Vd = {Vd:.6f} V   (= -E2 ; ขั้ว*ลบ*อยู่ที่ปม d)")

    # ---------------- ขั้นที่ 6 ----------------
    head("ขั้นที่ 6 — ตรวจ KCL, สมดุลกำลังไฟฟ้า และผลของ G4")

    iG1 = G1 * (Va - Vb)
    iG3 = G3 * Vb
    iG2 = G2 * (Vc - Vd)
    iG4 = G4 * Vd
    print("\n  กระแสแต่ละกิ่ง:")
    print(f"    i_G1 = G1(Va-Vb) = {G1}*({Va:.6f} - {Vb:.6f}) = {iG1:>12.6f} A")
    print(f"    i_G3 = G3*Vb     = {G3}*{Vb:.6f}              = {iG3:>12.6f} A")
    print(f"    i_G2 = G2(Vc-Vd) = {G2}*({Vc:.6f} - ({Vd:.6f})) = {iG2:>12.6f} A")
    print(f"    i_G4 = G4*Vd     = {G4}*{Vd:.6f}              = {iG4:>12.6f} A"
          + ("   <- ติดลบ = ไหลสวนทิศอ้างอิง" if iG4 < 0 else ""))

    print(f"\n  ตรวจ KCL ที่ supernode (b,c):  i_G1 =?= i_G3 + i_G2")
    print(f"    {iG1:.9f} =?= {iG3:.9f} + {iG2:.9f} = {iG3+iG2:.9f}")
    print(f"    ผลต่าง = {iG1-(iG3+iG2):.3e}   {'OK' if abs(iG1-(iG3+iG2)) < 1e-9 else 'FAIL'}")

    # กระแสของแหล่งจ่าย หาจากรอยตัดที่ 1, 3, 4
    iE1 = -iG1                 # cut1: i_E1 + i_G1 = 0
    iE3 = -iG2                 # cut3: i_E3 + i_G2 = 0
    iE2 = iG2 - iG4            # cut4: i_E2 - i_G2 + i_G4 = 0
    print("\n  กระแสของแหล่งจ่าย (จากรอยตัดที่ 1, 3, 4):")
    print(f"    i_E1 = {iE1:>12.6f} A (ทิศ a->e)  -> จ่ายออกที่ขั้วบวก {abs(iE1):.6f} A")
    print(f"    i_E3 = {iE3:>12.6f} A (ทิศ c->b)")
    print(f"    i_E2 = {iE2:>12.6f} A (ทิศ d->e)")

    pG = [G1 * (Va - Vb) ** 2, G3 * Vb ** 2, G2 * (Vc - Vd) ** 2, G4 * Vd ** 2]
    pdis = sum(pG)
    pE = [-(Va * iE1), -((Vc - Vb) * iE3), -(Vd * iE2)]
    pdel = sum(pE)
    print("\n  สมดุลกำลังไฟฟ้า:")
    for nm, p in zip(["G1", "G3", "G2", "G4"], pG):
        print(f"    P({nm}) = {p:>12.6f} W")
    print(f"    {'รวมสูญเสีย':<8} = {pdis:>12.6f} W")
    for nm, p in zip(["E1", "E3", "E2"], pE):
        print(f"    P({nm}) = {p:>12.6f} W  (จ่ายออก)")
    print(f"    {'รวมจ่าย':<9} = {pdel:>12.6f} W")
    print(f"\n    ผลต่าง = {pdel - pdis:.3e} W"
          f"   {'สมดุล (ระดับ machine epsilon)' if abs(pdel-pdis) < 1e-9 else 'ไม่สมดุล!'}")

    print("\n  ทดสอบว่า G4 มีผลต่อแรงดันปมหรือไม่ — กวาดค่า G4:")
    print(f"    {'G4 [mho]':>12}{'Va':>12}{'Vb':>12}{'Vc':>12}{'Vd':>12}{'i_G4 [A]':>14}")
    print("  " + SUB)
    for g4 in (0.0, G4, 5.0, 1000.0):
        r = route_A_closed_form(G1, G2, G3, g4, E1, E2, E3)
        print(f"    {g4:>12.4g}" + "".join(f"{x:>12.6f}" for x in r)
              + f"{g4*r[3]:>14.4f}")
    print("\n    -> แรงดันทั้งสี่ปมไม่ขยับเลย แม้ G4 เปลี่ยน 2,500 เท่า")
    print("       เพราะ Vd ถูกตรึงด้วยแหล่งจ่ายอุดมคติ E2 ที่ต่อขนานกับ G4")
    print("       G4 มีผลแค่ทำให้ E2 ต้องจ่ายกระแสเพิ่มเท่านั้น")

    # ---------------- ตรวจไขว้แบบสุ่ม ----------------
    if a.trials > 0:
        head(f"ตรวจไขว้แบบสุ่ม {a.trials} ชุด")
        rng = np.random.default_rng(7)
        worst = 0.0
        for _ in range(a.trials):
            g = rng.uniform(0.05, 5.0, 4)
            e = rng.uniform(-30.0, 30.0, 3)
            r1 = route_A_closed_form(*g, *e)
            r2 = route_B_cutset(QG, *g, *e)[0]
            r3 = route_C_linear_system(*g, *e)[0]
            worst = max(worst, np.abs(r1 - r2).max(), np.abs(r1 - r3).max())
        print(f"\n  สุ่ม G1..G4 ใน [0.05, 5] mho และ E1..E3 ใน [-30, 30] V")
        print(f"  ความคลาดเคลื่อนสูงสุดระหว่างทั้งสามเส้นทาง = {worst:.3e}")
        print(f"  machine epsilon ของ float64 = {np.finfo(float).eps:.3e}")
        print(f"  {'ผ่าน: สูตรที่พิสูจน์ด้วยมือถูกต้อง' if worst < 1e-9 else 'ไม่ผ่าน!'}")

    # ---------------- สรุป ----------------
    head("สรุปคำตอบสุดท้าย")
    print(f"""
  รูปเชิงสัญลักษณ์:
      Va = E1
      Vb = (G1*E1 - G2*E2 - G2*E3) / (G1 + G2 + G3)
      Vc = (G1*E1 - G2*E2 + (G1+G3)*E3) / (G1 + G2 + G3)
      Vd = -E2

  แทนค่าตัวเลข (G1={G1}, G2={G2}, G3={G3}, G4={G4} mho; E1={E1}, E2={E2}, E3={E3} V):
      Va = {Va:.6f} V
      Vb = {Vb:.6f} V
      Vc = {Vc:.6f} V
      Vd = {Vd:.6f} V

  ข้อสังเกตสำคัญ 3 ข้อสำหรับห้องสอบ:
    1. G4 ไม่ปรากฏในคำตอบแรงดันเลย เพราะ Vd ถูกตรึงด้วยแหล่งจ่ายอุดมคติ E2
    2. รอยตัดพื้นฐานของกิ่ง G3 ให้สมการเดียวกับ KCL ที่ supernode (b,c) เป๊ะ
    3. Vd = -E2 (ไม่ใช่ +E2) เพราะขั้วลบของ E2 อยู่ที่ปม d
""")

    if a.json:
        out = dict(
            parameters=dict(G1=G1, G2=G2, G3=G3, G4=G4, E1=E1, E2=E2, E3=E3),
            node_voltages=dict(Va=float(Va), Vb=float(Vb), Vc=float(Vc), Vd=float(Vd)),
            branch_currents=dict(i_G1=float(iG1), i_G3=float(iG3),
                                 i_G2=float(iG2), i_G4=float(iG4),
                                 i_E1=float(iE1), i_E3=float(iE3), i_E2=float(iE2)),
            power=dict(dissipated=float(pdis), delivered=float(pdel),
                       residual=float(pdel - pdis)),
            graph=dict(nodes=n, branches=b, twigs=TWIGS, links=LINKS,
                       det_At=float(det), Q=Q.tolist(), B=B.tolist(),
                       QYQt=M.tolist(), orthogonal=bool(np.allclose(QBt, 0))),
            notes=("G4 does not appear in any node voltage because Vd is pinned by the "
                   "ideal source E2 connected in parallel with G4."),
        )
        path = args_path = os.path.join(HERE, a.json)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2, ensure_ascii=False)
        print(f"  บันทึก JSON -> {args_path}\n")

    print("ดูคำอธิบายเต็มได้ที่ CLAUDE_SOLUTION.md")
    print("ซ้อมตอบสอบปากเปล่าได้ที่ interactive_dashboard.html แท็บที่ 5\n")


if __name__ == "__main__":
    main()
