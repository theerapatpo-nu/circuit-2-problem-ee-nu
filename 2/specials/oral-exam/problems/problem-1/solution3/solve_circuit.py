#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solve_circuit.py — เฉลยโจทย์สอบปากเปล่า 303212 ฉบับตรวจสอบได้ทุกตัวเลข
===============================================================================

โจทย์: วงข่ายความต้านทานต่อกับแบตเตอรี่ (ดู ../oral_exam_problem.md)

    KCL ที่ Node 1 :  i(t) = i_s(t) + v(t)/R_L
    KVL ลูปซ้าย    :  v(t) = v_s(t) - i(t)*R_i
    โมเดลแบตเตอรี่  :  v_s(t) = E_o - K*q + A_a*exp(-B_a*q) - A_b*exp(-B_b*(Q_n - q))
    โดย               q(t) = integral(0..t) i dα   และ   Q_n = integral(0..t_n) i dα

สคริปต์นี้ทำ 6 อย่าง เรียงตามลำดับที่ควรอธิบายในห้องสอบ:

    ขั้นที่ 1  ตรวจ KCL ครบทั้ง 2,753 แถว                 -> i(t) = 0.74 A
    ขั้นที่ 2  อินทิเกรตหาประจุ (สูตร + เชิงตัวเลข)        -> q(t) = 0.74t,  Q_n = 2664 C
    ขั้นที่ 3  หาหน้าต่างเชิงเส้นด้วยเกณฑ์ 1 mV
    ขั้นที่ 4  ทำตามลายมืออาจารย์ทีละบรรทัด (piecewise asymptotic)
    ขั้นที่ 5  ฟิตด้วยคอมพิวเตอร์ (Variable Projection)
    ขั้นที่ 6  วิเคราะห์ identifiability ของ (E_o, R_i)

ต้องการแค่ NumPy เท่านั้น — ไม่ต้องใช้ SciPy (เขียน optimizer เองเพื่อให้รันได้ทุกเครื่อง)
matplotlib และ pandas เป็นตัวเลือกเสริม ถ้าไม่มีก็ยังรันได้ครบ

วิธีรัน:
    python3 solve_circuit.py
    python3 solve_circuit.py --csv out.csv --plot fig.png
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np

# ----------------------------------------------------------------------------
# ค่าคงที่จากโจทย์
# ----------------------------------------------------------------------------
R_L = 10.0        # [Ω]  ความต้านทานภาระ
T_N = 3600.0      # [s]  เวลาอ้างอิงของความจุตามฉลาก

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(HERE, "..", "data303212qz02.md")

SEP = "=" * 78
SUB = "-" * 78


def head(title: str) -> None:
    print("\n" + SEP)
    print(title)
    print(SEP)


# ----------------------------------------------------------------------------
# อ่านข้อมูล
# ----------------------------------------------------------------------------
def load_data(path: str) -> np.ndarray:
    """อ่านตาราง markdown 3 คอลัมน์: t [s] | v(t) [V] | is(t) [A]

    เขียนแบบ parser ธรรมดาโดยตั้งใจ เพื่อไม่ต้องพึ่ง pandas —
    บรรทัดที่แปลงเป็น float ไม่ได้ (หัวตาราง, เส้นคั่น, front-matter) จะถูกข้าม
    """
    if not os.path.exists(path):
        sys.exit(f"หาไฟล์ข้อมูลไม่เจอ: {path}")

    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) != 3:
                continue
            try:
                rows.append([float(c) for c in cells])
            except ValueError:
                continue          # หัวตาราง หรือเส้นคั่น --- | --- | ---

    if not rows:
        sys.exit(f"อ่านไฟล์ได้ แต่ไม่พบแถวข้อมูลที่เป็นตัวเลขใน {path}")

    return np.array(rows, dtype=float)


# ----------------------------------------------------------------------------
# ขั้นที่ 1 — KCL
# ----------------------------------------------------------------------------
def step1_kcl(t: np.ndarray, v: np.ndarray, i_s: np.ndarray) -> np.ndarray:
    head("ขั้นที่ 1 — สมการโหนด (KCL) ที่ Node 1 :  i(t) = i_s(t) + v(t)/R_L")

    i = i_s + v / R_L

    print("\nสุ่มตรวจ 3 จุดตามที่อาจารย์ทำในเฉลย:")
    for k in (0, 10, 100):
        print(f"  t = {k:>3d} s :  {i_s[k]!r}")
        print(f"             + {v[k]!r} / 10")
        print(f"             = {i[k]:.15f} A")

    print("\nแต่ 3 จุดไม่ใช่หลักฐาน — นี่คือหลักฐาน (ตรวจครบทุกแถว):")
    print(f"  จำนวนแถว          = {len(i)}")
    print(f"  ค่าต่ำสุด          = {i.min():.20f} A")
    print(f"  ค่าสูงสุด          = {i.max():.20f} A")
    print(f"  ค่าเฉลี่ย           = {i.mean():.20f} A")
    print(f"  ส่วนเบี่ยงเบนมาตรฐาน = {i.std():.6e} A   <- ระดับ machine epsilon")
    print(f"  max|i - 0.74|      = {np.abs(i - 0.74).max():.6e} A")
    print(f"\n  machine epsilon ของ float64 = {np.finfo(float).eps:.6e}")
    print("\n  => i(t) = 0.74 A คงที่ทุกวินาที (constant-current discharge)")

    print("\nแล้ว i_s ทำอะไรอยู่? มันชดเชยให้กระแสรวมคงที่:")
    print(f"  ที่ t=0    : โหลดกิน v/R_L = {v[0]/R_L:.6f} A , i_s = {i_s[0]:.6f} A")
    print(f"  ที่ t=2752 : โหลดกิน v/R_L = {v[-1]/R_L:.6f} A , i_s = {i_s[-1]:.6f} A")
    print(f"  โหลดกินน้อยลง {v[0]/R_L - v[-1]/R_L:+.6f} A "
          f", i_s เพิ่มขึ้น {i_s[-1] - i_s[0]:+.6f} A  -> หักล้างกันพอดี")

    return i


# ----------------------------------------------------------------------------
# ขั้นที่ 2 — ประจุ
# ----------------------------------------------------------------------------
def step2_charge(t: np.ndarray, i: np.ndarray):
    head("ขั้นที่ 2 — อินทิเกรตหาประจุ  q(t) = ∫₀ᵗ i(α)dα  และ  Q_n")

    I0 = float(np.median(i))                      # 0.74 A
    q_formula = I0 * t                            # เพราะกระแสคงที่
    Q_n = I0 * T_N

    # ตรวจด้วยวิธีเชิงตัวเลข (trapezoidal) โดยไม่เชื่อสูตร
    dt = np.diff(t)
    q_trap = np.concatenate([[0.0], np.cumsum(0.5 * (i[1:] + i[:-1]) * dt)])

    print(f"\n  กระแสคงที่ I0 = {I0} A  =>  ดึงออกนอกอินทิกรัลได้")
    print(f"  q(t) = ∫₀ᵗ {I0} dα = {I0}·[α]₀ᵗ = {I0}t   [C]")
    print(f"  ตรวจหน่วย: [A]·[s] = [C/s]·[s] = [C]  OK")
    print(f"\n  Q_n = ∫₀^{T_N:.0f} {I0} dα = {I0} × {T_N:.0f} = {Q_n:.1f} C"
          f"  = {Q_n/3600:.2f} Ah = {Q_n/3.6:.0f} mAh")

    print("\n  ตรวจสูตรด้วย trapezoidal rule จากข้อมูลจริง (ไม่เชื่อสูตร):")
    print(f"    max|q_trap - {I0}t| = {np.abs(q_trap - q_formula).max():.3e} C  -> สูตรถูก")

    print(f"\n  ระวัง! ข้อมูลมีถึง t = {t[-1]:.0f} s เท่านั้น แต่ t_n = {T_N:.0f} s")
    print(f"    q ปลายข้อมูล = {q_formula[-1]:.2f} C = {100*q_formula[-1]/Q_n:.1f}% ของ Q_n")
    print(f"    ประจุคงเหลือ  = {Q_n - q_formula[-1]:.2f} C  -> SoC = "
          f"{100*(1 - q_formula[-1]/Q_n):.1f}%")
    print("    Q_n เป็น 'ค่าตามฉลากผู้ผลิต' (rated capacity) ตามนิยามในโจทย์")
    print("    ไม่ใช่การ extrapolate ข้อมูลการวัด")

    print("\n  พิสูจน์เทอมสุดท้ายของโมเดล (คุณสมบัติการแบ่งช่วง):")
    print("    ∫₀^tn = ∫₀ᵗ + ∫ₜ^tn   =>   Q_n = q(t) + ∫ₜ^tn i dα")
    print(f"    ∴ ∫ₜ^tn i(α)dα = Q_n - q(t) = {Q_n:.0f} - {I0}t   ('ประจุที่ยังเหลือ')")

    return I0, q_formula, Q_n


# ----------------------------------------------------------------------------
# โมเดล
# ----------------------------------------------------------------------------
def v_model(q, C0, K, Aa, Ba, Ab, Bb, Qn):
    """v(t) = (E_o - i·R_i) - K·q + A_a·e^(-B_a·q) - A_b·e^(-B_b·(Q_n - q))"""
    return C0 - K * q + Aa * np.exp(-Ba * q) - Ab * np.exp(-Bb * (Qn - q))


def rmse_of(q, v, p, Qn):
    r = v_model(q, p["C0"], p["K"], p["Aa"], p["Ba"], p["Ab"], p["Bb"], Qn) - v
    return float(np.sqrt(r @ r / len(r))), float(np.abs(r).max()), r


# ----------------------------------------------------------------------------
# ขั้นที่ 3 — หน้าต่างเชิงเส้น
# ----------------------------------------------------------------------------
def step3_window(Aa, Ba, Ab, Bb, Qn, I0, tol=1e-3):
    head(f"ขั้นที่ 3 — หาหน้าต่างเชิงเส้นด้วยเกณฑ์เชิงปริมาณ (เทอม < {tol*1000:.0f} mV)")

    q_lo = math.log(Aa / tol) / Ba                 # เทอมต้นเล็กกว่า tol เมื่อ q > q_lo
    q_hi = Qn - math.log(Ab / tol) / Bb            # เทอมปลายเล็กกว่า tol เมื่อ q < q_hi

    print(f"\n  A_a·e^(-B_a·q) < {tol*1000:.0f} mV  เมื่อ  q > {q_lo:7.1f} C  (t > {q_lo/I0:6.0f} s)")
    print(f"  A_b·e^(-B_b·(Q_n-q)) < {tol*1000:.0f} mV  เมื่อ  q < {q_hi:7.1f} C  (t < {q_hi/I0:6.0f} s)")
    print(f"\n  => หน้าต่างเชิงเส้น: q ∈ [{q_lo:.0f}, {q_hi:.0f}] C   หรือ   t ∈ [{q_lo/I0:.0f}, {q_hi/I0:.0f}] s")

    ok = q_lo < 740 and 1036 < q_hi
    print(f"\n  ช่วงที่อาจารย์ใช้ q ∈ [740, 1036] C อยู่ในหน้าต่างนี้ไหม? -> {'ใช่' if ok else 'ไม่ใช่'}")
    print("  (นี่คือคำตอบเวลากรรมการถามว่า 'ทำไมถึงเลือกช่วงนั้น')")
    return q_lo, q_hi


# ----------------------------------------------------------------------------
# ขั้นที่ 4 — เดินตามลายมืออาจารย์
# ----------------------------------------------------------------------------
def step4_hand(t, v, q, Qn, I0):
    head("ขั้นที่ 4 — วิธีคำนวณด้วยมือตามเฉลยอาจารย์ (Piecewise Asymptotic)")

    # --- 4.1  K จากความชันช่วงเชิงเส้น -------------------------------------
    ta, tb = 1000, 1400
    qa, qb = I0 * ta, I0 * tb
    slope = (v[ta] - v[tb]) / (qa - qb)
    K_hand = 2.724e-4                       # ค่าที่อาจารย์เขียน (ปัดจาก slope)

    print(f"\n[4.1] ความชันช่วงเชิงเส้น — ใช้ t = {ta} s และ {tb} s")
    print(f"      q({ta}) = {qa:.0f} C ,  q({tb}) = {qb:.0f} C")
    print(f"      v({ta}) = {v[ta]:.7f} V ,  v({tb}) = {v[tb]:.7f} V")
    print(f"      -K = Δv/Δq = ({v[ta]:.5f} - {v[tb]:.5f}) / ({qa:.0f} - {qb:.0f}) = {slope:.6e}")
    print(f"      K  = {-slope:.6e} V/C   -> อาจารย์เขียน {K_hand:.4e} V/C   [ตรงกัน]")

    # --- 4.2  E_o' จากจุดตัดแกน --------------------------------------------
    v1000_read = 3.8353                     # ค่าที่อาจารย์อ่านจากตาราง
    C0_hand = v1000_read + K_hand * qa
    print(f"\n[4.2] จุดตัดแกน — แทนกลับที่ q = {qa:.0f} C")
    print(f"      {v1000_read} = -({K_hand:.4e})({qa:.0f}) + E_o'")
    print(f"      E_o' = E_o - 0.74·R_i = {C0_hand:.6f} V")
    print(f"      (อาจารย์อ่าน v = {v1000_read} ค่าจริงในตาราง = {v[ta]:.6f} "
          f"ต่างกัน {abs(v1000_read - v[ta])*1000:.2f} mV จากการปัดเศษ)")

    # --- 4.3  R_i ภายใต้สมมติฐาน -------------------------------------------
    Eo_assumed = 4.0801                     # อาจารย์สมมติ E_o ≈ v(100)
    Ri_hand = (Eo_assumed - C0_hand) / I0
    print(f"\n[4.3] R_i — ต้องใส่สมมติฐานเพิ่ม เพราะข้อมูลอย่างเดียวหาไม่ได้")
    print(f"      สมมติ E_o ≈ v(100) = {Eo_assumed} V  (ค่าจริงในตาราง = {v[100]:.6f})")
    print(f"      R_i = (E_o - E_o')/0.74 = ({Eo_assumed} - {C0_hand:.6f})/{I0} "
          f"= {Ri_hand:.4f} Ω")
    print(f"      *** นี่คือค่า 'ประมาณ' ไม่ใช่ 'คำนวณ' — ดูขั้นที่ 6 ***")

    # --- 4.4  A_a ที่ q = 0 -------------------------------------------------
    Aa_hand = 0.13723
    print(f"\n[4.4] A_a — ที่ t=0, q=0 : e^(-B_a·0)=1 และเทอมปลาย ≈ 0")
    print(f"      v(0) = E_o' + A_a  =>  {v[0]:.4f} = {C0_hand:.5f} + A_a")
    print(f"      A_a = {Aa_hand} V")

    # --- 4.5  B_a : จุดที่เกิดปัญหา ----------------------------------------
    v100_read = 4.081
    q100 = I0 * 100

    lhs_without = v100_read - C0_hand
    Ba_prof = -math.log(lhs_without / Aa_hand) / q100

    lhs_with = v100_read - C0_hand + K_hand * q100
    Ba_fixed = -math.log(lhs_with / Aa_hand) / q100

    print(f"\n[4.5] B_a — *** นี่คือบรรทัดที่ต้องอธิบายให้ได้ในห้องสอบ ***")
    print(f"\n      สมการที่อาจารย์เขียน (ไม่มีเทอม -K·q):")
    print(f"        v(100) = E_o' + A_a·e^(-B_a·{q100:.0f})")
    print(f"        {v100_read} - {C0_hand:.5f} = {lhs_without:.6f}")
    print(f"        e^(-{q100:.0f}·B_a) = {lhs_without/Aa_hand:.6f}")
    print(f"        B_a = {Ba_prof:.6f} 1/C     <- ตรงกับเฉลย 0.01533")

    print(f"\n      แต่สมการเต็มมีเทอม -K·q(t) อยู่ด้วย:")
    print(f"        ขนาดเทอมที่หายไป = K·q(100) = {K_hand:.4e} × {q100:.0f} "
          f"= {K_hand*q100*1000:.1f} mV")
    print(f"        เทียบกับแรงดันรวม 4 V        -> {100*K_hand*q100/4:.2f}%  (ดูเล็ก)")
    print(f"        เทียบกับเทอมที่กำลังแก้หา {lhs_with*1000:.1f} mV "
          f"-> {100*K_hand*q100/lhs_with:.1f}%  (ใหญ่เกินไป!)")

    print(f"\n      ทำใหม่โดยเก็บเทอมนั้นไว้:")
    print(f"        {v100_read} = {C0_hand:.6f} - {K_hand*q100:.6f} + {Aa_hand}·e^(-{q100:.0f}·B_a)")
    print(f"        e^(-{q100:.0f}·B_a) = {lhs_with/Aa_hand:.6f}")
    print(f"        B_a = {Ba_fixed:.6f} 1/C     <- ตรงกับค่าฟิตคอมพิวเตอร์")

    # --- 4.6  A_b, B_b ------------------------------------------------------
    t1, t2 = 2700, 2750
    q1, q2 = I0 * t1, I0 * t2
    rem1, rem2 = Qn - q1, Qn - q2
    d1 = C0_hand - K_hand * q1 - 3.05          # ค่าที่อาจารย์อ่าน v(2700)=3.05
    d2 = C0_hand - K_hand * q2 - 2.8244        # ค่าที่อาจารย์อ่าน v(2750)=2.8244

    Bb_exact = -math.log(d1 / d2) / (rem1 - rem2)
    Bb_hand = 0.0107                    # อาจารย์ปัดเศษ
    Ab_recon = d1 / math.exp(-rem1 * Bb_hand)     # ที่เราสร้างขึ้นใหม่จากลูกโซ่ข้างบน
    Ab_written = 551.176                # ค่าที่อาจารย์เขียนไว้จริงในเฉลย

    print(f"\n[4.6] A_b และ B_b — ที่ปลายกราฟ เทอม A_a ตายสนิทแล้ว")
    print(f"      (e^(-B_a·{q1:.0f}) = {math.exp(-Ba_prof*q1):.2e} ≈ 0)")
    print(f"      t={t1}: q={q1:.0f} C, Q_n-q={rem1:.0f} C -> A_b·e^(-{rem1:.0f}B_b) = {d1:.5f}   ...(1)")
    print(f"      t={t2}: q={q2:.0f} C, Q_n-q={rem2:.0f} C -> A_b·e^(-{rem2:.0f}B_b) = {d2:.5f}   ...(2)")
    print(f"\n      เทคนิค: (1)/(2) ทำให้ A_b หายไปเอง")
    print(f"        e^(-{rem1-rem2:.0f}·B_b) = {d1:.5f}/{d2:.5f} = {d1/d2:.5f}")
    print(f"        B_b = {Bb_exact:.6f} 1/C   -> อาจารย์ปัดเป็น {Bb_hand}")
    print(f"      แทนกลับ (1): A_b = {d1:.5f}/e^(-{rem1:.0f}×{Bb_hand}) = {Ab_recon:.3f} V")
    print(f"      อาจารย์เขียนไว้ในเฉลยว่า A_b = {Ab_written} V "
          f"(ต่างจากที่เราสร้างใหม่ {abs(Ab_written-Ab_recon):.2f} V = "
          f"{100*abs(Ab_written-Ab_recon)/Ab_written:.2f}%)")
    print(f"\n      *** ทำไมถึงต่างกัน? เพราะ A_b ไวต่อการปัดเศษของ B_b มาก ***")
    print(f"        A_b = {d1:.5f}·e^({rem1:.0f}·B_b)  =>  δA_b/A_b = {rem1:.0f}·δB_b")
    print(f"        ความคลาดเคลื่อนของ B_b ถูกขยาย {rem1:.0f} เท่า")
    print(f"        ใช้ B_b ไม่ปัดเศษ ({Bb_exact:.6f}) จะได้ A_b = "
          f"{d1/math.exp(-rem1*Bb_exact):.2f} V")
    print(f"        => เวลารายงาน ต้องรายงาน A_b คู่กับ B_b เสมอ")
    print(f"           และปริมาณที่มีความหมายจริงคือ 'ผลคูณ' A_b·e^(-B_b(Q_n-q)) ในช่วงข้อมูล")

    # ชุด 'hand' ใช้ตัวเลข "ที่อาจารย์เขียนไว้จริง" ทุกตัว (ปัดเศษแล้ว)
    # เพราะนั่นคือคำตอบที่กรรมการถืออยู่ — ตัวเลขจึงตรงกับ CLAUDE_SOLUTION.md
    # และ interactive_dashboard.html ทุกหลัก  ส่วนค่าที่เราสร้างใหม่แบบไม่ปัดเศษ
    # เก็บไว้ในคีย์ *_reconstructed เพื่อให้ตรวจสอบย้อนกลับได้
    hand = dict(C0=C0_hand, K=K_hand, Aa=Aa_hand, Ba=0.01533,
                Ab=Ab_written, Bb=Bb_hand, Ri=Ri_hand, Eo_assumed=Eo_assumed,
                Ba_reconstructed=Ba_prof, Ab_reconstructed=Ab_recon,
                Bb_reconstructed=Bb_exact)
    fixed = dict(hand, Ba=round(Ba_fixed, 6), Ba_reconstructed=Ba_fixed)
    return hand, fixed


# ----------------------------------------------------------------------------
# ขั้นที่ 5 — ฟิตด้วยคอมพิวเตอร์ (Variable Projection)
# ----------------------------------------------------------------------------
def _linear_part(q, v, Ba, Bb, Qn):
    """ตรึง (B_a, B_b) แล้วโมเดลเป็นเชิงเส้นใน (C0, K, A_a, A_b) -> แก้ปิดรูป"""
    X = np.column_stack([
        np.ones_like(q),                  # C0
        -q,                               # K
        np.exp(-Ba * q),                  # A_a
        -np.exp(-Bb * (Qn - q)),          # A_b
    ])
    coef, *_ = np.linalg.lstsq(X, v, rcond=None)
    resid = X @ coef - v
    return coef, float(resid @ resid)


def step5_fit(q, v, Qn):
    head("ขั้นที่ 5 — ฟิตด้วยคอมพิวเตอร์: Variable Projection (NumPy อย่างเดียว)")

    print("\n  แนวคิด: ถ้ารู้ (B_a, B_b) แล้ว โมเดลเป็นเชิงเส้นใน (C0, K, A_a, A_b)")
    print("          ซึ่งแก้ได้ปิดรูปด้วย least-squares -> ปัญหา 6 มิติยุบเหลือ 2 มิติ")
    print("          [Golub & Pereyra 1973]\n")

    # (ก) ค้นหาแบบกริดหยาบ เพื่อหาแอ่งที่ถูกต้องก่อน (กัน local minimum)
    grid = np.linspace(0.002, 0.030, 113)
    best = None
    for Ba in grid:
        for Bb in grid:
            _, sse = _linear_part(q, v, Ba, Bb, Qn)
            if best is None or sse < best[0]:
                best = (sse, Ba, Bb)
    print(f"  (ก) กริดหยาบ {len(grid)}×{len(grid)} จุด -> "
          f"B_a≈{best[1]:.5f}, B_b≈{best[2]:.5f}, SSE={best[0]:.4e}")

    # (ข) ปรับละเอียดด้วย pattern search (ลดขนาดก้าวเรื่อยๆ จนถึงความละเอียดเครื่อง)
    p = np.array([best[1], best[2]], dtype=float)
    step = np.array([1e-3, 1e-3])
    f = lambda x: _linear_part(q, v, x[0], x[1], Qn)[1]
    fp = f(p)
    for _ in range(4000):
        improved = False
        for j in (0, 1):
            for s in (+1.0, -1.0):
                cand = p.copy()
                cand[j] += s * step[j]
                if cand[j] <= 0:
                    continue
                fc = f(cand)
                if fc < fp:
                    p, fp = cand, fc
                    improved = True
        if not improved:
            step *= 0.5
            if step.max() < 1e-17:
                break

    Ba, Bb = float(p[0]), float(p[1])
    coef, sse = _linear_part(q, v, Ba, Bb, Qn)
    C0, K, Aa, Ab = (float(c) for c in coef)
    resid = v_model(q, C0, K, Aa, Ba, Ab, Bb, Qn) - v
    rmse = float(np.sqrt(sse / len(v)))

    print(f"  (ข) ปรับละเอียดด้วย pattern search -> ลู่เข้า\n")
    print(f"  E_o' = C0 = {C0:.15f}   V")
    print(f"  K         = {K:.15e} V/C")
    print(f"  A_a       = {Aa:.15f}   V")
    print(f"  B_a       = {Ba:.15f}   1/C")
    print(f"  A_b       = {Ab:.12f}      V")
    print(f"  B_b       = {Bb:.15f}   1/C")
    print(f"\n  SSE      = {sse:.4e} V²")
    print(f"  RMSE     = {rmse:.4e} V")
    print(f"  max|r|   = {np.abs(resid).max():.4e} V")

    print(f"\n  *** อ่านผลให้เป็น: RMSE ระดับ 1e-13 V คือระดับ machine epsilon ***")
    print(f"      เครื่องมือวัดจริงไม่มีทางละเอียดขนาดนี้")
    print(f"      => ข้อมูลชุดนี้ถูกสร้างจากสมการนี้เอง ไม่ใช่ข้อมูลวัดจริง")
    print(f"      (ข้อมูลแล็บจริงจะได้ RMSE ราว 1e-3 ถึง 1e-2 V จาก noise/อุณหภูมิ/hysteresis)")

    # โครงสร้างที่ซ่อนอยู่ในพารามิเตอร์
    print(f"\n  ตรวจโครงสร้างพารามิเตอร์ — B·Q_n ออกมาเป็นเลขซ้ำ:")
    print(f"      B_a × Q_n = {Ba*Qn:.10f}   (= 300/11)")
    print(f"      B_b × Q_n = {Bb*Qn:.10f}   (= 200/7)")
    print(f"      3/B_a = {3/Ba:.4f} C = {100*3/Ba/Qn:.3f}% ของ Q_n")
    print(f"      3/B_b = {3/Bb:.4f} C = {100*3/Bb/Qn:.3f}% ของ Q_n")
    print(f"  => ทั้งคู่อยู่ในรูป B = 3/Q_exp ซึ่งเป็นธรรมเนียมของโมเดล Shepherd/Tremblay")
    print(f"     (ที่ q = Q_exp เทอมเลขชี้กำลังเหลือ e^-3 = 4.98% ≈ 'ตายไป 95%')")
    print(f"     ผู้ออกข้อสอบตั้งช่วงเลขชี้กำลังต้นไว้ 11.0% และช่วงหน้าผาไว้ 10.5% ของความจุ")

    return dict(C0=C0, K=K, Aa=Aa, Ba=Ba, Ab=Ab, Bb=Bb), resid, rmse


# ----------------------------------------------------------------------------
# ขั้นที่ 6 — identifiability
# ----------------------------------------------------------------------------
def step6_identifiability(C0, I0):
    head("ขั้นที่ 6 — ทำไม E_o กับ R_i ถึงแยกจากกันไม่ได้ (Structural Non-identifiability)")

    print(f"\n  เพราะ i(t) = {I0} A คงที่ เทอม i·R_i จึงเป็นค่าคงที่ด้วย")
    print(f"  มันจึงรวมกับ E_o เป็นก้อนเดียว:  E_o' = E_o - {I0}·R_i = {C0:.12f} V")
    print(f"  ข้อมูลเห็นแค่ 'ผลต่าง' ก้อนนี้ ไม่เห็นตัวใครตัวมัน")

    print(f"\n  Jacobian:")
    print(f"      ∂v̂/∂E_o = 1")
    print(f"      ∂v̂/∂R_i = -i(t) = {-I0}   (คงที่ทุกแถว)")

    J = np.column_stack([np.ones(5), np.full(5, -I0)])
    print(f"  => สองคอลัมน์เป็นสัดส่วนกันพอดี -> rank(J) = {np.linalg.matrix_rank(J)} (ไม่ใช่ 2)")
    print(f"     JᵀJ เป็น singular : det = {np.linalg.det(J.T @ J):.3e}")

    print(f"\n  คำตอบที่เป็นไปได้มีเป็นอนันต์ บนเส้น  E_o = {C0:.6f} + {I0}·R_i :")
    print(f"    {'R_i [Ω]':>10}  {'E_o [V]':>12}  {'i·R_i [mV]':>12}   ทำนาย v(t) เท่ากันไหม")
    for Ri in (0.0, 0.0584, 0.2, 1.0, 10.0):
        print(f"    {Ri:>10.4f}  {C0 + I0*Ri:>12.6f}  {I0*Ri*1000:>12.1f}   เท่ากันทุกจุด")

    print(f"\n  *** จุดสำคัญ: แก้ไม่ได้ด้วยการเพิ่มข้อมูล ***")
    print(f"      ต่อให้มีข้อมูลล้านจุดที่ไม่มี noise เลย ก็ยังแยกไม่ออก")
    print(f"      ตราบใดที่กระแสยังคงที่  (ต่างจาก practical non-identifiability)")
    print(f"\n  วิธีแก้ในโลกจริง: Current Pulse Test / HPPC")
    print(f"      1) พักแบตจนแรงดันนิ่ง -> วัด OCV ได้ตรงๆ (i=0 เทอม iR_i หาย)")
    print(f"      2) จ่ายพัลส์ Δi ทันที -> แรงดันกระโดด Δv เร็วเกินกว่าเคมีจะตอบสนอง")
    print(f"      3) R_i = |Δv/Δi| ตอน t->0⁺   แล้วจึงได้ E_o = E_o' + {I0}·R_i")
    print(f"\n  หลักการ: ความต้านทานเห็นได้จาก 'การเปลี่ยนแปลง' ของกระแส ไม่ใช่จากตัวกระแสเอง")


# ----------------------------------------------------------------------------
# เปรียบเทียบ
# ----------------------------------------------------------------------------
def compare(q, v, Qn, hand, fixed, fit):
    head("ตารางเปรียบเทียบ: มือ (อาจารย์)  vs  มือ (แก้เทอม Kq)  vs  คอมพิวเตอร์")

    rows = [
        ("E_o'", hand["C0"], fixed["C0"], fit["C0"], "V"),
        ("K",    hand["K"],  fixed["K"],  fit["K"],  "V/C"),
        ("A_a",  hand["Aa"], fixed["Aa"], fit["Aa"], "V"),
        ("B_a",  hand["Ba"], fixed["Ba"], fit["Ba"], "1/C"),
        ("A_b",  hand["Ab"], fixed["Ab"], fit["Ab"], "V"),
        ("B_b",  hand["Bb"], fixed["Bb"], fit["Bb"], "1/C"),
    ]
    print(f"\n  {'param':<7}{'มือ (อาจารย์)':>18}{'มือ (แก้ Kq)':>18}"
          f"{'คอมพิวเตอร์':>20}{'ผิด %':>11}  หน่วย")
    print("  " + SUB)
    for name, h, fx, ft, unit in rows:
        err = abs(h - ft) / abs(ft) * 100
        flag = "  <-- ดูขั้นที่ 4.5" if name == "B_a" else ""
        print(f"  {name:<7}{h:>18.8g}{fx:>18.8g}{ft:>20.12g}{err:>10.3f}%  {unit}{flag}")

    print("\n  คุณภาพเมื่อแทนกลับกับข้อมูลจริงทั้ง %d จุด:" % len(v))
    print(f"  {'ชุดพารามิเตอร์':<26}{'RMSE [V]':>14}{'max|r| [V]':>15}"
          f"{'RMSE ช่วง t≤400':>18}")
    print("  " + SUB)
    early = slice(1, 401)
    for label, p in (("ลายมืออาจารย์", hand), ("แก้เทอม Kq", fixed), ("คอมพิวเตอร์", fit)):
        rm, mx, r = rmse_of(q, v, p, Qn)
        re = float(np.sqrt(r[early] @ r[early] / (early.stop - early.start)))
        print(f"  {label:<24}{rm:>15.4e}{mx:>15.4e}{re:>18.4e}")

    _, _, rh = rmse_of(q, v, hand, Qn)
    k = int(np.argmax(np.abs(rh)))
    rm_h = float(np.sqrt(rh @ rh / len(rh)))
    _, _, rf = rmse_of(q, v, fixed, Qn)
    rm_f = float(np.sqrt(rf @ rf / len(rf)))

    print(f"\n  ความคลาดเคลื่อนสูงสุดของชุดลายมือ = {abs(rh[k])*1000:.2f} mV ที่ t = {k} s")
    print(f"  ขนาดเทอม K·q(74) ที่ถูกตัดทิ้ง      = {hand['K']*0.74*100*1000:.2f} mV  <- ตรงกัน")
    print(f"  แก้เทอมแล้ว RMSE ดีขึ้น {rm_h/rm_f:.1f} เท่า")

    print("\n  วิธีพูดในห้องสอบ (ห้ามพูดว่า 'อาจารย์ผิด'):")
    print("    \"อาจารย์ใช้การประมาณตัดเทอม Kq ทิ้งในช่วงต้นครับ ซึ่งสมเหตุสมผลเพราะ")
    print("     20 mV เทียบกับ 4 V คือ 0.5% แต่ผมตรวจดูแล้วพบว่าถ้าเทียบกับเทอม")
    print("     เลขชี้กำลังที่กำลังแก้หา ซึ่งมีขนาด 64 mV มันคิดเป็น 31% ครับ")
    print("     ผมจึงลองเก็บเทอมนั้นไว้ แล้ว RMSE ดีขึ้นจาก 5.4 เป็น 0.25 mV ครับ\"")


# ----------------------------------------------------------------------------
# ผลลัพธ์เสริม
# ----------------------------------------------------------------------------
def extras(t, v, i, q, Qn, fit, Ri):
    head("ปริมาณเสริมที่กรรมการชอบถาม")

    p = v * i
    energy_J = float(np.trapezoid(p, t)) if hasattr(np, "trapezoid") else float(np.trapz(p, t))
    I0 = float(np.median(i))

    print(f"\n  พลังงานที่จ่ายตลอดการทดลอง = ∫v·i dt = {energy_J:.2f} J = {energy_J/3600:.5f} Wh")
    print(f"  แรงดันเฉลี่ย                = {v.mean():.5f} V")
    print(f"  กำลังที่ t=0 / ปลาย         = {p[0]:.4f} W / {p[-1]:.4f} W")
    print(f"  แรงดันตกใน R_i              = i·R_i = {I0*Ri*1000:.2f} mV")
    print(f"  กำลังสูญเป็นความร้อนใน R_i   = i²R_i = {I0*I0*Ri*1000:.2f} mW")
    print(f"  SoC ปลายข้อมูล              = {100*(1-q[-1]/Qn):.1f}%")

    print(f"\n  ขนาดของแต่ละเทอม ณ จุดสำคัญ (ใช้ค่าฟิต):")
    print(f"  {'t [s]':>7}{'q [C]':>10}{'SoC':>8}{'v [V]':>10}"
          f"{'K·q':>10}{'A_a term':>11}{'A_b term':>11}")
    print("  " + SUB)
    for k in (0, 100, 293, 650, 1000, 1400, 1932, 2400, 2700, 2752):
        qq = q[k]
        print(f"  {int(t[k]):>7}{qq:>10.1f}{100*(1-qq/Qn):>7.1f}%{v[k]:>10.4f}"
              f"{fit['K']*qq:>10.5f}{fit['Aa']*math.exp(-fit['Ba']*qq):>11.6f}"
              f"{fit['Ab']*math.exp(-fit['Bb']*(Qn-qq)):>11.6f}")


def save_csv(path, t, v, i_s, i, q, Qn, fit):
    vm = v_model(q, fit["C0"], fit["K"], fit["Aa"], fit["Ba"], fit["Ab"], fit["Bb"], Qn)
    arr = np.column_stack([t, v, i_s, i, q, 100 * (1 - q / Qn), vm, vm - v, v * i])
    np.savetxt(path, arr, delimiter=",", fmt="%.12g",
               header="t_s,v_volt,is_amp,i_amp,q_coulomb,soc_percent,"
                      "v_model_volt,residual_volt,power_watt", comments="")
    print(f"\n  บันทึก CSV ({len(t)} แถว) -> {path}")


def save_plot(path, t, v, i_s, i, q, Qn, hand, fixed, fit):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n  ข้ามการวาดกราฟ: ไม่มี matplotlib (pip install matplotlib)")
        print("  ใช้ interactive_dashboard.html แทนได้ — มีกราฟโต้ตอบครบกว่า")
        return

    fig, ax = plt.subplots(2, 2, figsize=(13, 8.5))

    ax[0, 0].plot(t, i, lw=2.2, color="#15803d", label="i = 0.74 A")
    ax[0, 0].plot(t, i_s, lw=1.6, color="#7c3aed", label="$i_s(t)$")
    ax[0, 0].plot(t, v / R_L, lw=1.6, color="#c2740b", label="$v/R_L$")
    ax[0, 0].set(xlabel="t [s]", ylabel="current [A]", title="KCL: i = $i_s$ + v/$R_L$ = 0.74 A")
    ax[0, 0].legend(); ax[0, 0].grid(alpha=.3)

    ax[0, 1].plot(q, v, lw=4, color="#94a3b8", alpha=.55, label="measured")
    ax[0, 1].plot(q, v_model(q, **{k: fit[k] for k in ("C0", "K", "Aa", "Ba", "Ab", "Bb")}, Qn=Qn),
                  lw=1.4, color="#2563eb", label="fitted model")
    ax[0, 1].axvspan(481, 1430, color="#15803d", alpha=.12, label="linear window")
    ax[0, 1].set(xlabel="q [C]", ylabel="v [V]", title="v vs q + linear window")
    ax[0, 1].legend(); ax[0, 1].grid(alpha=.3)

    ax[1, 0].plot(q, fit["Aa"] * np.exp(-fit["Ba"] * q), color="#c2740b", label="$A_a e^{-B_a q}$")
    ax[1, 0].plot(q, fit["Ab"] * np.exp(-fit["Bb"] * (Qn - q)), color="#dc2626",
                  label="$A_b e^{-B_b(Q_n-q)}$")
    ax[1, 0].plot(q, fit["K"] * q, "--", color="#94a3b8", label="$K q$")
    ax[1, 0].axvspan(481, 1430, color="#15803d", alpha=.12)
    ax[1, 0].set(xlabel="q [C]", ylabel="term size [V]", title="ขนาดของแต่ละเทอม")
    ax[1, 0].legend(); ax[1, 0].grid(alpha=.3)

    _, _, rh = rmse_of(q, v, hand, Qn)
    _, _, rf = rmse_of(q, v, fixed, Qn)
    ax[1, 1].plot(t, rh * 1000, color="#dc2626", label="hand ($B_a$=0.01533)")
    ax[1, 1].plot(t, rf * 1000, color="#15803d", label="hand + fixed $K q$")
    ax[1, 1].set(xlabel="t [s]", ylabel="residual [mV]", title="ความคลาดเคลื่อน")
    ax[1, 1].legend(); ax[1, 1].grid(alpha=.3)

    fig.tight_layout()
    fig.savefig(path, dpi=130)
    print(f"  บันทึกกราฟ -> {path}")


# ----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=DEFAULT_DATA, help="ไฟล์ตาราง markdown")
    ap.add_argument("--csv", nargs="?", const="computed_data.csv",
                    help="บันทึกผลคำนวณเป็น CSV")
    ap.add_argument("--plot", nargs="?", const="figures.png",
                    help="บันทึกกราฟสรุป (ต้องมี matplotlib)")
    ap.add_argument("--json", nargs="?", const="fit_results.json",
                    help="บันทึกพารามิเตอร์เป็น JSON")
    args = ap.parse_args()

    print(SEP)
    print("เฉลยโจทย์สอบปากเปล่า 303212 — วงข่ายความต้านทานกับโมเดลแบตเตอรี่")
    print("solution3 / solve_circuit.py")
    print(SEP)

    D = load_data(args.data)
    t, v, i_s = D[:, 0], D[:, 1], D[:, 2]
    print(f"\nอ่านข้อมูลจาก: {os.path.normpath(args.data)}")
    print(f"  {len(D)} แถว, t = {t[0]:.0f} .. {t[-1]:.0f} s, R_L = {R_L} Ω, t_n = {T_N:.0f} s")

    i = step1_kcl(t, v, i_s)
    I0, q, Qn = step2_charge(t, i)
    hand, fixed = step4_hand(t, v, q, Qn, I0)
    fit, resid, rmse = step5_fit(q, v, Qn)
    step3_window(fit["Aa"], fit["Ba"], fit["Ab"], fit["Bb"], Qn, I0)
    step6_identifiability(fit["C0"], I0)
    compare(q, v, Qn, hand, fixed, fit)
    extras(t, v, i, q, Qn, fit, hand["Ri"])

    head("สรุปคำตอบสุดท้าย")
    print(f"""
  ได้จากวงจรโดยตรง (ไม่มีข้อโต้แย้ง):
      i(t) = {I0} A                คงที่ทุกจุด ทั้ง {len(i)} แถว
      q(t) = {I0}t  [C]
      Q_n  = {Qn:.0f} C = {Qn/3600:.2f} Ah = {Qn/3.6:.0f} mAh

  พารามิเตอร์แบตเตอรี่ (ค่าฟิตจากข้อมูลครบทุกจุด):
      E_o' = E_o - {I0}·R_i = {fit['C0']:.12f} V
      K    = {fit['K']:.12e} V/C
      A_a  = {fit['Aa']:.12f} V
      B_a  = {fit['Ba']:.12f} 1/C
      A_b  = {fit['Ab']:.9f} V
      B_b  = {fit['Bb']:.12f} 1/C
      RMSE = {rmse:.4e} V

  ค่าตามเฉลยอาจารย์ (คำตอบที่กรรมการถืออยู่):
      E_o' = {hand['C0']:.6f} V , K = {hand['K']:.4e} V/C , A_a = {hand['Aa']} V
      B_a  = {hand['Ba']:.5f} 1/C , A_b = {hand['Ab']:.3f} V , B_b = {hand['Bb']} 1/C
      R_i  = {hand['Ri']:.4f} Ω  (ประมาณ ภายใต้สมมติฐาน E_o ≈ v(100) = {hand['Eo_assumed']} V)

  E_o กับ R_i แยกจากกันไม่ได้จากข้อมูลชุดนี้ — คำตอบอยู่บนเส้น
      E_o = {fit['C0']:.6f} + {I0}·R_i
""")

    if args.csv:
        save_csv(os.path.join(HERE, args.csv), t, v, i_s, i, q, Qn, fit)
    if args.plot:
        save_plot(os.path.join(HERE, args.plot), t, v, i_s, i, q, Qn, hand, fixed, fit)
    if args.json:
        out = dict(
            i_ampere=I0, q_formula="q(t) = 0.74*t", Qn_coulomb=Qn, Qn_Ah=Qn / 3600,
            rows=int(len(D)), R_L_ohm=R_L, t_n_second=T_N,
            computer_fit=fit, computer_rmse_volt=rmse,
            hand_professor=hand, hand_with_Kq_term=fixed,
            identifiability=("E_o and R_i are NOT separately identifiable at constant "
                             "current; only C0 = E_o - 0.74*R_i is."),
            family=f"E_o = {fit['C0']:.12f} + {I0}*R_i",
        )
        path = os.path.join(HERE, args.json)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2, ensure_ascii=False)
        print(f"  บันทึก JSON -> {path}")

    print("\nดูคำอธิบายเต็มได้ที่ CLAUDE_SOLUTION.md")
    print("ซ้อมตอบสอบปากเปล่าได้ที่ interactive_dashboard.html แท็บที่ 5\n")


if __name__ == "__main__":
    main()
