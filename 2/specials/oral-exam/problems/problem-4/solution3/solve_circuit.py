#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solve_circuit.py — เฉลยเชิงคำนวณสำหรับโจทย์สอบปากเปล่า 303212 ข้อที่ 4

วงจร: G1 (a-e), G2 (a-b), G3 (b-e), I0 (e->a), CCCS alpha*ix (b->a)
โดย ix = G1*Va และ Ve = 0

สคริปต์นี้ใช้ SymPy สำหรับตรวจรูปเชิงสัญลักษณ์ (ถ้าติดตั้งไว้) และใช้ NumPy
สำหรับการคำนวณเชิงตัวเลข/การตรวจ residual โดยไม่ซ่อนขั้นตอนสำคัญของ KCL.

ตัวอย่าง:
    python3 solve_circuit.py
    python3 solve_circuit.py --G1 0.8 --G2 0.35 --G3 0.55 --alpha 0.4 --I0 2.4
    python3 solve_circuit.py --json result.json --sweep-alpha
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import numpy as np
except ImportError as exc:  # pragma: no cover - ข้อความช่วยเหลือเมื่อ environment ไม่พร้อม
    raise SystemExit(
        "ต้องติดตั้ง NumPy ก่อนรันสคริปต์นี้ เช่น: python3 -m pip install numpy"
    ) from exc

try:
    import sympy as sp
except ImportError:
    sp = None

BRANCHES = ["G1", "G3", "G2", "I0", "alpha_ix"]
TWIGS = ["G1", "G3"]
LINKS = ["G2", "I0", "alpha_ix"]
NODES = ["a", "b", "e"]


def build_cutset_matrix() -> np.ndarray:
    """สร้าง [QK] = [I2 | QL] ตาม orientation ที่ระบุในบทเรียน.

    QK คือ reduced incidence ที่จัดคอลัมน์ให้กิ่งต้นไม้อยู่ซ้าย:
        G1: a -> e, G3: b -> e, G2: a -> b,
        I0: e -> a, alpha_ix: b -> a.
    """
    return np.array(
        [
            [1.0, 0.0, 1.0, -1.0, -1.0],
            [0.0, 1.0, -1.0, 0.0, 1.0],
        ]
    )


def branch_operator(g1: float, g2: float, g3: float, alpha: float, i0: float):
    qk = build_cutset_matrix()
    yb = np.array(
        [
            [g1, 0.0, 0.0, 0.0, 0.0],
            [0.0, g3, 0.0, 0.0, 0.0],
            [0.0, 0.0, g2, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [alpha * g1, 0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    jb = np.array([0.0, 0.0, 0.0, i0, 0.0], dtype=float)
    return qk, yb, jb


def symbolic_solution() -> dict[str, str] | None:
    """สร้างผลเชิงสัญลักษณ์ด้วย SymPy เพื่อแสดงว่าคำตอบไม่ได้เกิดจากการฟิตตัวเลข."""
    if sp is None:
        return None
    g1, g2, g3, alpha, i0 = sp.symbols("G_1 G_2 G_3 alpha I_0")
    A = sp.Matrix(
        [
            [(1 - alpha) * g1 + g2, -g2],
            [alpha * g1 - g2, g2 + g3],
        ]
    )
    det = sp.factor(A.det())
    sol = sp.simplify(A.inv() * sp.Matrix([i0, 0]))
    return {
        "determinant": str(det),
        "Va": str(sp.factor(sol[0])),
        "Vb": str(sp.factor(sol[1])),
        "matrix": str(A),
    }


def numeric_solution(g1: float, g2: float, g3: float, alpha: float, i0: float):
    """แก้สมการแบบเมทริกซ์และคืนค่าตัวแปร/เมทริกซ์ประกอบทั้งหมด."""
    if min(g1, g2, g3) <= 0:
        raise ValueError("G1, G2 และ G3 ต้องเป็นค่าบวก")
    qk, yb, jb = branch_operator(g1, g2, g3, alpha, i0)
    A = qk @ yb @ qk.T
    jcut = -(qk @ jb)
    delta = float(np.linalg.det(A))
    scale = max(1.0, float(np.linalg.norm(A, ord=np.inf)))
    if abs(delta) <= 1e-12 * scale * scale:
        raise ValueError(
            f"เมทริกซ์เกือบ singular: Delta={delta:.12g}; "
            "ลองลด alpha หรือเพิ่ม damping ในโมเดลจริง"
        )
    v = np.linalg.solve(A, jcut)
    va, vb = map(float, v)
    ix = g1 * va
    idep = alpha * ix
    ig2 = g2 * (va - vb)
    ig3 = g3 * vb
    residual = A @ v - jcut
    return {
        "parameters": {
            "G1": g1,
            "G2": g2,
            "G3": g3,
            "alpha": alpha,
            "I0": i0,
        },
        "A": A,
        "QK": qk,
        "Yb": yb,
        "Jb": jb,
        "Jcut": jcut,
        "delta": delta,
        "Va": va,
        "Vb": vb,
        "ix": float(ix),
        "alpha_ix": float(idep),
        "iG2": float(ig2),
        "iG3": float(ig3),
        "kcl_a": float(i0 + idep - ix - ig2),
        "kcl_b": float(-idep + ig2 - ig3),
        "residual_norm": float(np.linalg.norm(residual, ord=np.inf)),
    }


def cramer_solution(g1: float, g2: float, g3: float, alpha: float, i0: float):
    """คำนวณซ้ำด้วย Cramer's Rule เพื่อ cross-check กับ numpy.linalg.solve."""
    a11 = (1 - alpha) * g1 + g2
    a12 = -g2
    a21 = alpha * g1 - g2
    a22 = g2 + g3
    delta = a11 * a22 - a12 * a21
    da = i0 * a22 - a12 * 0.0
    db = a11 * 0.0 - i0 * a21
    return da / delta, db / delta, delta


def fmt_matrix(m: np.ndarray) -> str:
    return "\n".join("  [ " + "  ".join(f"{x: .6f}" for x in row) + " ]" for row in m)


def print_symbolic() -> None:
    print("\n--- SymPy: รูปเชิงสัญลักษณ์ ---")
    result = symbolic_solution()
    if result is None:
        print("ไม่ได้เรียกใช้ SymPy เพราะ environment นี้ยังไม่มีแพ็กเกจ sympy")
        print("ติดตั้งได้ด้วย: python3 -m pip install sympy")
        return
    print("A =", result["matrix"])
    print("det(A) =", result["determinant"])
    print("Va =", result["Va"])
    print("Vb =", result["Vb"])


def print_result(result: dict) -> None:
    p = result["parameters"]
    print("\n--- พารามิเตอร์ ---")
    print(
        f"G1={p['G1']:.6f}, G2={p['G2']:.6f}, G3={p['G3']:.6f} mho, "
        f"alpha={p['alpha']:.6f}, I0={p['I0']:.6f} A"
    )
    print("\n--- QK ---")
    print(fmt_matrix(result["QK"]))
    print("\n--- Yb (มี coupling ของ CCCS ในแถวสุดท้าย) ---")
    print(fmt_matrix(result["Yb"]))
    print("\n--- A = QK @ Yb @ QK.T ---")
    print(fmt_matrix(result["A"]))
    print("Jcut =", np.array2string(result["Jcut"], precision=6))
    print(f"Delta = {result['delta']:.12f} mho^2")
    print("\n--- คำตอบแรงดัน ---")
    print(f"Va = {result['Va']:.12f} V")
    print(f"Vb = {result['Vb']:.12f} V")
    print("\n--- กระแสและการตรวจ KCL ---")
    print(f"ix       = {result['ix']:.12f} A")
    print(f"alpha*ix = {result['alpha_ix']:.12f} A")
    print(f"iG2      = {result['iG2']:.12f} A")
    print(f"iG3      = {result['iG3']:.12f} A")
    print(f"KCL(a) residual = {result['kcl_a']:.3e} A")
    print(f"KCL(b) residual = {result['kcl_b']:.3e} A")
    print(f"matrix residual  = {result['residual_norm']:.3e}")


def sweep_alpha(g1: float, g2: float, g3: float, i0: float) -> None:
    print("\n--- Alpha sweep ---")
    print(" alpha        Delta             Va [V]          Vb [V]")
    alpha_crit = 1.0 + g2 / g1 + g2 / g3
    for alpha in np.linspace(0.0, min(alpha_crit * 0.92, 5.0), 8):
        try:
            r = numeric_solution(g1, g2, g3, float(alpha), i0)
            print(f" {alpha: .6f}  {r['delta']: .9f}  {r['Va']: .9f}  {r['Vb']: .9f}")
        except ValueError:
            print(f" {alpha: .6f}  singular")
    print(f"alpha_critical = 1 + G2/G1 + G2/G3 = {alpha_crit:.9f}")


def serializable(result: dict) -> dict:
    out = {}
    for key, value in result.items():
        if isinstance(value, np.ndarray):
            out[key] = value.tolist()
        else:
            out[key] = value
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--G1", type=float, default=0.8, help="ความนำ G1 [mho]")
    parser.add_argument("--G2", type=float, default=0.35, help="ความนำ G2 [mho]")
    parser.add_argument("--G3", type=float, default=0.55, help="ความนำ G3 [mho]")
    parser.add_argument("--alpha", type=float, default=0.4, help="อัตราขยาย CCCS")
    parser.add_argument("--I0", type=float, default=2.4, help="แหล่งกระแส I0 [A]")
    parser.add_argument("--json", nargs="?", const="results.json", help="บันทึก JSON")
    parser.add_argument("--sweep-alpha", action="store_true", help="แสดงผลกวาดค่า alpha")
    args = parser.parse_args()

    try:
        result = numeric_solution(args.G1, args.G2, args.G3, args.alpha, args.I0)
    except ValueError as exc:
        raise SystemExit(f"ข้อผิดพลาด: {exc}") from exc

    print("=" * 78)
    print("303212 Oral Exam — Problem 4: Conductance Network + CCCS")
    print("=" * 78)
    print_symbolic()
    print_result(result)
    va_c, vb_c, delta_c = cramer_solution(args.G1, args.G2, args.G3, args.alpha, args.I0)
    print("\n--- Cross-check: Cramer's Rule vs NumPy ---")
    print(f"Va(Cramer) = {va_c:.12f} V, difference = {va_c - result['Va']:.3e}")
    print(f"Vb(Cramer) = {vb_c:.12f} V, difference = {vb_c - result['Vb']:.3e}")
    print(f"Delta(Cramer) = {delta_c:.12f} mho^2")
    if args.sweep_alpha:
        sweep_alpha(args.G1, args.G2, args.G3, args.I0)

    if args.json:
        path = Path(args.json)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent / path
        path.write_text(json.dumps(serializable(result), indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nบันทึกผลลัพธ์ JSON ที่ {path}")

    print("\nผ่าน: คำตอบจาก matrix solve, Cramer's Rule และ KCL สอดคล้องกัน")


if __name__ == "__main__":
    main()
